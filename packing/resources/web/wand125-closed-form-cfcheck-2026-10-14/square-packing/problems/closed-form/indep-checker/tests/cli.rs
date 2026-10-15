use serde_json::{json, Value};
use std::{
    fs,
    path::PathBuf,
    process::Command,
    sync::atomic::{AtomicUsize, Ordering},
};
static COUNTER: AtomicUsize = AtomicUsize::new(0);
struct Scratch(PathBuf);
impl Scratch {
    fn new() -> Self {
        let p = PathBuf::from(format!(
            "tests/scratch_{}_{}",
            std::process::id(),
            COUNTER.fetch_add(1, Ordering::Relaxed)
        ));
        fs::create_dir_all(&p).unwrap();
        Self(p)
    }
}
impl Drop for Scratch {
    fn drop(&mut self) {
        fs::remove_dir_all(&self.0).unwrap();
    }
}
fn cli(args: &[&str]) -> (i32, Value) {
    let out = Command::new(env!("CARGO_BIN_EXE_cfcheck"))
        .args(args)
        .args(["--threads", "2"])
        .output()
        .unwrap();
    let text = String::from_utf8(out.stdout).unwrap();
    let value = serde_json::from_str(text.lines().next().expect("JSON output")).expect(&text);
    (out.status.code().unwrap(), value)
}
#[test]
fn coverage_cli() {
    let (code, r) = cli(&["coverage", "tests/fixtures/intervals.json"]);
    assert_eq!(code, 0);
    assert_eq!(r["ok"], true);
    assert_eq!(r["inputs"][0]["sha256"].as_str().unwrap().len(), 64);
}
fn fixture(p: &Scratch) {
    let family =
        json!({"d0":"0","d1":"1/10","UA":"9/5","F":[["1/2","2","1/2","4","100"]],"T":[],"V":[]});
    fs::write(p.0.join("family.json"), family.to_string()).unwrap();
    fs::write(p.0.join("family_right.json"), family.to_string()).unwrap();
    fs::write(p.0.join("SHA256SUMS"), "").unwrap();
    let mut lines = String::new();
    for (a, b) in [("-1/2", "0"), ("0", "1/2")] {
        lines+=&json!({"root":["0","1/2","3","31/10",a,b,"0","1/10"],"leaves":[[["0","1/4","3","31/10",a,b,"0","1/10"],"EMPTY"],[["1/4","1/2","3","31/10",a,b,"0","1/10"],"CORE"]],"uncert":[],"f3d":[]}).to_string();
        lines += '\n'.to_string().as_str();
    }
    for name in ["top.rec", "left.rec", "straddle.rec", "right.rec"] {
        fs::write(p.0.join(name), &lines).unwrap();
    }
}
fn region(dir: &str) -> (i32, Value) {
    cli(&[
        "region",
        &format!("{dir}/family.json"),
        &format!("{dir}/top.rec"),
        "--bounds",
        "0",
        "1/2",
        "3",
        "31/10",
    ])
}
#[test]
fn mutation_pipeline() {
    let source = Scratch::new();
    fixture(&source);
    let dir = source.0.to_str().unwrap();
    let (code, r) = region(dir);
    assert_eq!(code, 0, "{r}");
    for mode in [
        "delete-leaf",
        "swap-kinds",
        "delete-root",
        "duplicate-root",
        "negative",
    ] {
        let out = Scratch::new();
        fixture(&out);
        let path = out.0.join("top.rec");
        let mut rows: Vec<Value> = fs::read_to_string(&path)
            .unwrap()
            .lines()
            .map(|line| serde_json::from_str(line).unwrap())
            .collect();
        match mode {
            "delete-leaf" => {
                rows[0]["leaves"].as_array_mut().unwrap().pop();
            }
            "swap-kinds" => {
                rows[0]["leaves"][0][1] = json!("CORE");
                rows[0]["leaves"][1][1] = json!("EMPTY");
            }
            "delete-root" => {
                rows.pop();
            }
            "duplicate-root" => rows.push(rows[0].clone()),
            "negative" => {
                let path = out.0.join("family.json");
                let mut family: Value =
                    serde_json::from_str(&fs::read_to_string(&path).unwrap()).unwrap();
                family["F"][0][4] = json!("-1");
                fs::write(path, family.to_string()).unwrap();
            }
            _ => unreachable!(),
        }
        fs::write(
            path,
            rows.iter()
                .map(|row| format!("{row}\n"))
                .collect::<String>(),
        )
        .unwrap();
        let (code, r) = region(out.0.to_str().unwrap());
        assert_eq!(code, 1, "{mode}: {r}");
        assert_eq!(r["ok"], false);
    }
}
#[test]
fn malformed_unknown_and_bounds() {
    let source = Scratch::new();
    fixture(&source);
    let dir = source.0.to_str().unwrap();
    let top = source.0.join("top.rec");
    let text = fs::read_to_string(&top).unwrap();
    fs::write(&top, text.replace("\"CORE\"", "\"CORE1\"")).unwrap();
    let (code, r) = region(dir);
    assert_eq!(code, 1);
    assert!(r["refusals"]
        .as_array()
        .unwrap()
        .iter()
        .any(|r| r["reason"].as_str().unwrap().contains("unknown kind")));
    fs::write(&top, &text).unwrap();
    let (code, _) = cli(&[
        "region",
        &format!("{dir}/family.json"),
        &format!("{dir}/top.rec"),
        "--bounds",
        "0",
        "3/5",
        "3",
        "31/10",
        "--max-roots",
        "0",
    ]);
    assert_eq!(code, 1);
    fs::write(&top, "not json\n").unwrap();
    assert_eq!(region(dir).0, 2);
}
#[test]
fn partial_label() {
    let source = Scratch::new();
    fixture(&source);
    let dir = source.0.to_str().unwrap();
    let (code, r) = cli(&[
        "region",
        &format!("{dir}/family.json"),
        &format!("{dir}/top.rec"),
        "--bounds",
        "0",
        "1/2",
        "3",
        "31/10",
        "--max-roots",
        "1",
    ]);
    assert_eq!(code, 0);
    assert_eq!(r["partial"], true);
    assert_eq!(r["roots"], 2);
    assert_eq!(r["leaves"], 4);
    assert_eq!(r["checked_leaf_kinds"]["CORE"], 1);
}

#[test]
fn unknown_family_key_is_reported() {
    let source = Scratch::new();
    fixture(&source);
    let path = source.0.join("family.json");
    let mut f: Value = serde_json::from_str(&fs::read_to_string(&path).unwrap()).unwrap();
    f["unrecognized"] = json!(true);
    fs::write(&path, f.to_string()).unwrap();
    let (code, r) = region(source.0.to_str().unwrap());
    assert_eq!(code, 1);
    assert!(r["extra_keys"][path.to_str().unwrap()]
        .as_array()
        .unwrap()
        .contains(&json!("unrecognized")));
}

#[test]
fn deadline_and_kind_selection() {
    let scratch = Scratch::new();
    fixture(&scratch);
    let family = scratch.0.join("family.json").to_string_lossy().into_owned();
    let record = scratch.0.join("top.rec").to_string_lossy().into_owned();
    let base = [
        "region",
        family.as_str(),
        record.as_str(),
        "--bounds",
        "0",
        "1/2",
        "3",
        "31/10",
    ];
    let mut args = base.to_vec();
    args.extend(["--deadline", "0"]);
    let (code, r) = cli(&args);
    assert_eq!(code, 1);
    assert_eq!(r["ok"], false);
    assert_eq!(r["roots"], 2);
    assert_eq!(r["leaves"], 4);
    assert_eq!(r["incomplete"], true);
    assert_eq!(r["refusals"], json!([]));
    assert_eq!(r["interruptions"][0]["reason"], "incomplete: deadline");
    let mut args = base.to_vec();
    args.extend(["--only-kinds", "CORE", "--max-leaves-per-kind", "1"]);
    let (code, r) = cli(&args);
    assert_eq!(code, 0);
    assert_eq!(r["partial"], true);
    assert_eq!(r["checked_leaf_kinds"]["CORE"], 1);
    assert!(r["checked_leaf_kinds"]["EMPTY"].is_null());
    assert_eq!(r["leaves"], 4);
    let mut args = base.to_vec();
    args.extend(["--only-kinds", "CORE1"]);
    assert_eq!(cli(&args).0, 2);
    let mut args = base.to_vec();
    args.extend(["--deadline", "-1"]);
    assert_eq!(cli(&args).0, 2);
}

#[test]
fn checkpoint_integrity_and_completion() {
    let scratch = Scratch::new();
    fixture(&scratch);
    let family = scratch.0.join("family.json").to_string_lossy().into_owned();
    let record = scratch.0.join("top.rec").to_string_lossy().into_owned();
    let progress = scratch.0.join("progress").to_string_lossy().into_owned();
    let base = [
        "region",
        &family,
        &record,
        "--bounds",
        "0",
        "1/2",
        "3",
        "31/10",
        "--progress-file",
        &progress,
    ];
    let (code, full) = cli(&base);
    assert_eq!(code, 0, "{full}");
    assert_eq!(full["partial"], false);
    let saved = fs::read_to_string(&progress).unwrap();
    let mut args = base.to_vec();
    args.extend(["--resume", "--max-roots", "0"]);
    let (code, resumed) = cli(&args);
    assert_eq!(code, 0, "{resumed}");
    assert_eq!(resumed["partial"], true);
    let mut full_resume = base.to_vec();
    full_resume.push("--resume");
    assert_eq!(cli(&full_resume).1["partial"], false);
    assert_eq!(resumed["resumed_roots"], 2);
    assert_eq!(resumed["checked_leaf_kinds"], full["checked_leaf_kinds"]);
    assert_eq!(cli(&base).0, 1); // no silent overwrite
                                 // Torn append recovery is append-only and never adds an acceptance.
    fs::write(&progress, format!("{saved}ACCEPT 3 abcd")).unwrap();
    assert_eq!(cli(&args).0, 0);
    assert_eq!(cli(&args).0, 0);
    assert!(fs::read_to_string(&progress).unwrap().starts_with(&saved));
    fs::write(&progress, saved.replace("\"CORE\":1", "\"CORE\":2")).unwrap();
    assert_eq!(cli(&args).0, 1);
    fs::write(&progress, &saved).unwrap();
    let original_family = fs::read_to_string(&family).unwrap();
    fs::write(&family, format!("{original_family} ")).unwrap();
    assert_eq!(cli(&args).0, 1);
    fs::write(&family, original_family).unwrap();
    // Domain checks still run even when every saved leaf is reused.
    let mut wrong = args.clone();
    wrong[5] = "3/5";
    let (code, bad) = cli(&wrong);
    assert_eq!(code, 1);
    assert_eq!(bad["resumed_roots"], 2);
    assert!(bad["refusals"][0]["reason"]
        .as_str()
        .unwrap()
        .contains("bounds mismatch"));
    // A selected subset must not become an accepted whole root.
    fs::remove_file(&progress).unwrap();
    let mut selected = base.to_vec();
    selected.extend(["--only-kinds", "CORE"]);
    assert_eq!(cli(&selected).0, 0);
    assert!(!fs::read_to_string(&progress).unwrap().contains("ACCEPT"));
    let (code, partial) = cli(&args);
    assert_eq!(code, 0);
    assert_eq!(partial["resumed_roots"], 0);
    assert_eq!(partial["partial"], true);
}
