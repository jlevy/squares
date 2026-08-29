//! Verify that sqsearch JSONL output reports exact pair-test counts.

use std::process::Command;

fn field(line: &str, name: &str) -> u64 {
    let marker = format!("\"{name}\":");
    let tail = line
        .split_once(&marker)
        .unwrap_or_else(|| panic!("missing {name} in {line}"))
        .1;
    let digits: String = tail.chars().take_while(char::is_ascii_digit).collect();
    digits
        .parse()
        .unwrap_or_else(|_| panic!("invalid {name} in {line}"))
}

fn stdout(args: &[&str]) -> String {
    let output = Command::new(env!("CARGO_BIN_EXE_sqsearch"))
        .args(args)
        .output()
        .expect("run sqsearch");
    assert!(
        output.status.success(),
        "sqsearch failed: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    String::from_utf8(output.stdout).expect("sqsearch stdout is UTF-8")
}

#[test]
fn jsonl_reports_exact_pair_tests_for_both_search_paths() {
    let ordinary = stdout(&[
        "--n",
        "4",
        "--seed",
        "7",
        "--chains",
        "2",
        "--threads",
        "1",
        "--steps",
        "3",
        "--max-restarts",
        "2",
        "--budget-moves",
        "6",
    ]);
    let ordinary_rows: Vec<_> = ordinary.lines().collect();
    let chains: Vec<_> = ordinary_rows
        .iter()
        .filter(|row| row.contains("\"kind\":\"chain\""))
        .collect();
    assert_eq!(chains.len(), 2);
    assert!(chains.iter().all(|row| field(row, "pair_tests") == 54));
    let ordinary_summary = ordinary_rows.last().expect("ordinary summary");
    assert_eq!(field(ordinary_summary, "pair_tests"), 108);
    assert!(ordinary_summary.contains("\"pair_tests_per_sec\":"));

    let seed_path = std::env::temp_dir().join(format!(
        "sqsearch-pair-meter-{}-{}.json",
        std::process::id(),
        std::thread::current().name().unwrap_or("test")
    ));
    std::fs::write(
        &seed_path,
        r#"{"x":[0.5,1.5,0.5,1.5],"y":[0.5,0.5,1.5,1.5],"t":[0,0,0,0]}"#,
    )
    .expect("write seed fixture");
    let entry = stdout(&[
        "--basin-entry",
        "--seed-config",
        seed_path.to_str().expect("UTF-8 temp path"),
        "--seed",
        "7",
        "--trials",
        "2",
        "--threads",
        "1",
        "--steps",
        "3",
        "--max-restarts",
        "2",
        "--budget-moves",
        "6",
        "--eps",
        "1e-4,1e-3",
    ]);
    std::fs::remove_file(&seed_path).expect("remove seed fixture");
    let entry_rows: Vec<_> = entry.lines().collect();
    let trials: Vec<_> = entry_rows
        .iter()
        .filter(|row| row.contains("\"kind\":\"entry\""))
        .collect();
    assert_eq!(trials.len(), 4);
    assert!(trials.iter().all(|row| field(row, "pair_tests") == 54));
    let entry_summary = entry_rows.last().expect("entry summary");
    assert_eq!(field(entry_summary, "pair_tests"), 216);
    assert!(entry_summary.contains("\"pair_tests_per_sec\":"));
}
