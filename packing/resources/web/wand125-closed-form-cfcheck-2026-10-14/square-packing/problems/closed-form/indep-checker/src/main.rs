use cfcheck::{
    parse_error,
    rat::{self, Q},
    report::Report,
    require, Result,
};
use serde_json::json;
use std::{
    collections::BTreeMap,
    path::{Path, PathBuf},
};
fn option(args: &mut Vec<String>, name: &str) -> Result<Option<String>> {
    if let Some(i) = args.iter().position(|s| s == name) {
        args.remove(i);
        if i == args.len() {
            return Err(parse_error(format!("{name} requires a value")));
        }
        Ok(Some(args.remove(i)))
    } else {
        Ok(None)
    }
}
fn flag(args: &mut Vec<String>, name: &str) -> bool {
    if let Some(i) = args.iter().position(|s| s == name) {
        args.remove(i);
        true
    } else {
        false
    }
}
fn number(s: Option<String>, default: usize) -> Result<usize> {
    s.map_or(Ok(default), |s| {
        s.parse::<usize>()
            .map_err(|_| parse_error("invalid unsigned integer argument"))
    })
}
fn validate_path(s: &str) -> Result<PathBuf> {
    let p = PathBuf::from(s);
    if p.is_absolute()
        || p.components()
            .any(|c| matches!(c, std::path::Component::ParentDir))
    {
        return Err(parse_error(
            "paths must be relative and remain inside this directory",
        ));
    }
    let cwd = std::env::current_dir()?;
    let resolved = if p.exists() {
        p.canonicalize()?
    } else {
        let parent = p
            .parent()
            .filter(|p| !p.as_os_str().is_empty())
            .unwrap_or(Path::new("."));
        parent
            .canonicalize()?
            .join(p.file_name().ok_or_else(|| parse_error("invalid path"))?)
    };
    if !resolved.starts_with(cwd) {
        return Err(parse_error("path resolves outside this directory"));
    }
    Ok(p)
}
fn run(mut args: Vec<String>, report: &mut Report) -> Result<()> {
    let deadline = option(&mut args, "--deadline")?
        .map(|s| {
            s.parse::<u64>()
                .map_err(|_| parse_error("--deadline requires unsigned seconds"))
        })
        .transpose()?;
    cfcheck::budget::start(deadline)?;
    let threads = number(option(&mut args, "--threads")?, 2)?;
    if threads == 0 {
        return Err(parse_error("--threads must be positive"));
    }
    let chunk_leaves_arg = option(&mut args, "--chunk-leaves")?;
    if chunk_leaves_arg.is_some() && !["region", "interval"].contains(&report.command.as_str()) {
        return Err(parse_error("--chunk-leaves requires region or interval"));
    }
    let chunk_leaves = number(chunk_leaves_arg, 64)?;
    if chunk_leaves == 0 {
        return Err(parse_error("--chunk-leaves must be positive"));
    }
    let max_roots = option(&mut args, "--max-roots")?
        .map(|s| number(Some(s), 0))
        .transpose()?;
    let progress_file = option(&mut args, "--progress-file")?
        .map(|s| validate_path(&s))
        .transpose()?;
    let resume = flag(&mut args, "--resume");
    if resume && progress_file.is_none() {
        return Err(parse_error("--resume requires --progress-file"));
    }
    if (progress_file.is_some() || resume)
        && !["region", "interval"].contains(&report.command.as_str())
    {
        return Err(parse_error("checkpoint flags require region or interval"));
    }
    let progress = flag(&mut args, "--progress");
    let only_kinds = option(&mut args, "--only-kinds")?.map(|s| {
        s.split(',')
            .map(str::to_owned)
            .collect::<std::collections::BTreeSet<_>>()
    });
    if let Some(ks) = &only_kinds {
        for k in ks {
            if !cfcheck::record::KINDS.contains(&k.as_str()) {
                return Err(parse_error(format!("unknown --only-kinds kind {k}")));
            }
        }
    }
    let max_per_kind = option(&mut args, "--max-leaves-per-kind")?
        .map(|s| number(Some(s), 0))
        .transpose()?;
    if (only_kinds.is_some() || max_per_kind.is_some())
        && !["region", "interval"].contains(&report.command.as_str())
    {
        return Err(parse_error(
            "leaf selection flags require region or interval",
        ));
    }

    match report.command.as_str() {
        "coverage" => {
            if args.len() != 1 {
                return Err(parse_error("usage: cfcheck coverage <intervals.json>"));
            }
            cfcheck::coverage::run(&validate_path(&args[0])?, report)
        }
        "family" | "interval" => {
            let ip = option(&mut args, "--intervals")?
                .ok_or_else(|| parse_error("--intervals required"))?;
            let index = number(option(&mut args, "--index")?, 0)?;
            if args.len() != 1 || index == 0 {
                return Err(parse_error(
                    "usage: cfcheck family|interval <asset_dir> --intervals <path> --index <i>",
                ));
            }
            let dir = validate_path(&args[0])?;
            let intervals = validate_path(&ip)?;
            if report.command == "family" {
                cfcheck::family::run(&dir, &intervals, index, report)?;
                for name in ["straddle", "left", "top", "right"] {
                    cfcheck::record::angular_range(&dir.join(format!("{name}.rec")), report)?;
                }
                return Ok(());
            }
            let iv = report.read_json(&intervals)?;
            let entry = cfcheck::coverage::rows(&iv)?
                .get(index - 1)
                .ok_or_else(|| parse_error("interval index outside range"))?
                .clone();
            let sums_path = dir.join("SHA256SUMS");
            let bytes = std::fs::read(&sums_path)?;
            report.add_bytes(&sums_path, &bytes);
            let s =
                std::str::from_utf8(&bytes).map_err(|_| parse_error("SHA256SUMS is not UTF-8"))?;
            let mut sums = BTreeMap::new();
            for line in s.lines() {
                let parts: Vec<_> = line.split_whitespace().collect();
                if parts.len() != 2 {
                    return Err(parse_error("invalid SHA256SUMS row"));
                }
                let name = parts[1].trim_start_matches('*');
                require(
                    [
                        "family.json",
                        "family_right.json",
                        "straddle.rec",
                        "left.rec",
                        "top.rec",
                        "right.rec",
                    ]
                    .contains(&name),
                    "unexpected SHA256SUMS filename",
                )?;
                require(
                    sums.insert(name.to_owned(), parts[0].to_owned()).is_none(),
                    "duplicate SHA256SUMS filename",
                )?;
            }
            require(sums.len() == 6, "SHA256SUMS must cover exactly six inputs")?;
            // Verify byte identities before any expensive mathematical replay.
            use sha2::{Digest, Sha256};
            use std::io::Read;
            for (name, hash) in &sums {
                let mut file = std::fs::File::open(dir.join(name))?;
                let mut digest = Sha256::new();
                let mut buffer = [0u8; 65536];
                loop {
                    let n = file.read(&mut buffer)?;
                    if n == 0 {
                        break;
                    }
                    digest.update(&buffer[..n]);
                }
                let actual = format!("{:x}", digest.finalize());
                require(actual == *hash, format!("SHA256SUMS mismatch: {name}"))?;
                let expected = match name.as_str() {
                    "family.json" => &entry["family_sha256"],
                    "family_right.json" => &entry["family_right_sha256"],
                    _ => &entry["regions"][name.trim_end_matches(".rec")]["sha256"],
                };
                require(
                    expected.as_str() == Some(actual.as_str()),
                    format!("interval hash mismatch: {name}"),
                )?;
            }
            cfcheck::family::run(&dir, &intervals, index, report)?;
            let structural = report.details.clone();
            let mut regions = serde_json::Map::new();
            for name in ["straddle", "left", "top", "right"] {
                let r = &entry["regions"][name];
                require(
                    r["file"].as_str() == Some(&format!("{name}.rec")),
                    "invalid region filename",
                )?;
                let fam = if name == "right" {
                    "family_right.json"
                } else {
                    "family.json"
                };
                let b = rat::array(&r["bounds"], 4)?.try_into().unwrap();
                let mut sub = Report::new("region");
                let region_progress = progress_file
                    .as_ref()
                    .map(|p| validate_path(&format!("{}.{name}", p.display())))
                    .transpose()?;
                cfcheck::record::run(
                    &dir.join(fam),
                    &dir.join(format!("{name}.rec")),
                    b,
                    threads,
                    chunk_leaves,
                    max_roots,
                    progress,
                    only_kinds.as_ref(),
                    max_per_kind,
                    region_progress.as_deref(),
                    resume && region_progress.as_ref().is_some_and(|p| p.exists()),
                    &mut sub,
                )?;
                if sub.roots != r["roots"].as_u64().unwrap_or(u64::MAX)
                    || sub.leaves != r["leaves"].as_u64().unwrap_or(u64::MAX)
                    || serde_json::to_value(&sub.leaf_kinds).unwrap() != r["leaf_kinds"]
                {
                    sub.error(
                        name,
                        cfcheck::refuse("published counts or kind counts mismatch"),
                    );
                }
                report.ok &= sub.ok;
                report.code = report.code.max(sub.code);
                report.roots += sub.roots;
                report.leaves += sub.leaves;
                for (k, v) in &sub.leaf_kinds {
                    *report.leaf_kinds.entry(k.clone()).or_default() += v;
                }
                for (k, v) in &sub.checked_leaf_kinds {
                    *report.checked_leaf_kinds.entry(k.clone()).or_default() += v;
                }
                report.inputs.append(&mut sub.inputs);
                report.refusals.append(&mut sub.refusals);
                report.partial |= sub.partial;
                report.incomplete |= sub.incomplete;
                report.resumed_roots += sub.resumed_roots;
                report.interruptions.append(&mut sub.interruptions);
                sub.finish();
                regions.insert(name.into(), sub.details);
            }
            for (name, hash) in sums {
                let path = dir.join(&name).to_string_lossy().into_owned();
                let actual = &report
                    .inputs
                    .iter()
                    .rev()
                    .find(|i| i.path == path)
                    .ok_or_else(|| cfcheck::refuse("unhashed input"))?
                    .sha256;
                require(actual == &hash, format!("SHA256SUMS mismatch: {name}"))?;
                let expected = match name.as_str() {
                    "family.json" => &entry["family_sha256"],
                    "family_right.json" => &entry["family_right_sha256"],
                    _ => &entry["regions"][name.trim_end_matches(".rec")]["sha256"],
                };
                require(
                    expected.as_str() == Some(actual),
                    format!("interval hash mismatch: {name}"),
                )?;
            }
            report.details = json!({"family":structural,"regions":regions});
            Ok(())
        }
        "region" => {
            let i = args
                .iter()
                .position(|s| s == "--bounds")
                .ok_or_else(|| parse_error("--bounds x0 x1 y0 y1 required"))?;
            if i + 4 >= args.len() {
                return Err(parse_error("four bounds required"));
            }
            let bounds: Vec<Q> = args
                .drain(i + 1..i + 5)
                .map(|s| rat::parse(&s))
                .collect::<Result<_>>()?;
            args.remove(i);
            if args.len() != 2 {
                return Err(parse_error(
                    "usage: cfcheck region <family> <record> --bounds x0 x1 y0 y1",
                ));
            }
            let b: [Q; 4] = bounds.try_into().unwrap();
            require(
                b[0] < b[1] && b[2] < b[3],
                "region bounds must have positive width",
            )?;
            cfcheck::record::run(
                &validate_path(&args[0])?,
                &validate_path(&args[1])?,
                b,
                threads,
                chunk_leaves,
                max_roots,
                progress,
                only_kinds.as_ref(),
                max_per_kind,
                progress_file.as_deref(),
                resume,
                report,
            )
        }
        _ => Err(parse_error("commands: coverage, family, region, interval")),
    }
}
fn main() {
    let mut args: Vec<_> = std::env::args().skip(1).collect();
    let mut report = Report::new(args.first().map(String::as_str).unwrap_or(""));
    if !args.is_empty() {
        args.remove(0);
    }
    let json_path = option(&mut args, "--json");
    let result = match &json_path {
        Err(e) => Err(e.clone()),
        Ok(_) => run(args, &mut report),
    };
    if let Err(e) = result {
        report.error("command", e);
    }
    if cfcheck::budget::expired() && report.ok {
        report.deadline("budget");
    }
    report.finish();
    if let Ok(Some(p)) = json_path {
        match validate_path(&p).and_then(|p| {
            std::fs::write(p, serde_json::to_vec_pretty(&report).unwrap())?;
            Ok(())
        }) {
            Ok(()) => {}
            Err(e) => report.error("JSON output", e),
        }
    }
    println!("{}", serde_json::to_string(&report).unwrap());
    if report.incomplete && report.refusals.is_empty() {
        println!("CFCHECK INCOMPLETE: deadline");
    } else if !report.ok {
        println!(
            "CFCHECK REFUSE: {}",
            report
                .refusals
                .first()
                .map(|r| r.reason.as_str())
                .unwrap_or("verification failed")
        );
    } else if report.partial {
        println!("CFCHECK PARTIAL");
    } else {
        println!("CFCHECK OK");
    }
    std::process::exit(report.code);
}
