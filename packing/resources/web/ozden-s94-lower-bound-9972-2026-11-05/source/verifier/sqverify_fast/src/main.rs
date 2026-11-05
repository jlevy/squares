//! `sqverify-fast`: verify a rectangle-density certificate direction by direction.
//!
//! ```text
//! sqverify-fast --candidate PATH --n N [--side P/Q] [--directions SPEC]
//!               [--threshold P/Q] [--threads K] [--max-nodes N] [--max-depth D]
//!               [--receipts DIR] [--confirm]
//! ```
//!
//! `SPEC` is `all` (the default), a range `a-b`, or a comma list. Standard
//! output is one JSON line per direction, then a summary line. The exit status
//! is 0 only when every requested direction is verified, 1 when one is refused
//! or unresolved, and 2 on an admission or usage error.

use std::path::PathBuf;
use std::process::ExitCode;
use std::sync::Mutex;
use std::sync::atomic::{AtomicUsize, Ordering};

use serde_json::json;
use sqverify_fast::certificate::{admit, read_json};
use sqverify_fast::exact::parse_rational;
use sqverify_fast::rotated::Limits;
use sqverify_fast::{premises, run_direction};

struct Options {
    candidate: PathBuf,
    n: u64,
    side: Option<String>,
    directions: String,
    threshold: Option<String>,
    threads: usize,
    limits: Limits,
    receipts: Option<PathBuf>,
    confirm: bool,
    probe: Option<String>,
}

fn parse_args() -> Result<Options, String> {
    let mut args = std::env::args().skip(1);
    let mut candidate = None;
    let mut n = None;
    let mut options = Options {
        candidate: PathBuf::new(),
        n: 0,
        side: None,
        directions: "all".into(),
        threshold: None,
        threads: 1,
        limits: Limits {
            max_nodes: 50_000_000,
            max_depth: 60,
            audit_every: 1024,
            inject_fault_at: None,
        },
        receipts: None,
        confirm: false,
        probe: None,
    };
    while let Some(flag) = args.next() {
        let mut value = || args.next().ok_or(format!("{flag} needs a value"));
        match flag.as_str() {
            "--candidate" => candidate = Some(PathBuf::from(value()?)),
            "--n" => n = Some(value()?.parse().map_err(|_| "--n must be an integer")?),
            "--side" => options.side = Some(value()?),
            "--directions" => options.directions = value()?,
            "--threshold" => options.threshold = Some(value()?),
            "--threads" => {
                options.threads = value()?
                    .parse()
                    .map_err(|_| "--threads must be an integer")?;
            }
            "--max-nodes" => {
                options.limits.max_nodes = value()?
                    .parse()
                    .map_err(|_| "--max-nodes must be an integer")?;
            }
            "--max-depth" => {
                options.limits.max_depth = value()?
                    .parse()
                    .map_err(|_| "--max-depth must be an integer")?;
            }
            "--audit-every" => {
                options.limits.audit_every = value()?
                    .parse()
                    .map_err(|_| "--audit-every must be an integer")?;
            }
            "--inject-fault-at-node" => {
                options.limits.inject_fault_at = Some(
                    value()?
                        .parse()
                        .map_err(|_| "--inject-fault-at-node must be an integer")?,
                );
            }
            "--receipts" => options.receipts = Some(PathBuf::from(value()?)),
            "--confirm" => options.confirm = true,
            "--probe" => options.probe = Some(value()?),
            "--help" | "-h" => return Err("usage: see the crate documentation".into()),
            other => return Err(format!("unknown argument {other}")),
        }
    }
    options.candidate = candidate.ok_or("--candidate is required")?;
    options.n = n.ok_or("--n is required")?;
    options.threads = options.threads.max(1);
    Ok(options)
}

fn parse_directions(spec: &str, count: u32) -> Result<Vec<u32>, String> {
    let mut out = Vec::new();
    if spec == "all" {
        return Ok((0..count).collect());
    }
    for part in spec.split(',') {
        if let Some((a, b)) = part.split_once('-') {
            let a: u32 = a
                .trim()
                .parse()
                .map_err(|_| format!("bad direction {part}"))?;
            let b: u32 = b
                .trim()
                .parse()
                .map_err(|_| format!("bad direction {part}"))?;
            out.extend(a..=b);
        } else {
            out.push(
                part.trim()
                    .parse()
                    .map_err(|_| format!("bad direction {part}"))?,
            );
        }
    }
    out.sort_unstable();
    out.dedup();
    if out.iter().any(|&r| r >= count) || out.is_empty() {
        return Err(format!("directions must lie in 0..{count}"));
    }
    Ok(out)
}

/// `--probe r,x,y[,dx,dy]`: the certified bound at a centre (or over a box)
/// beside the exact coverage at the centre, for differential tests.
fn probe(
    cert: &sqverify_fast::certificate::Certificate,
    spec: &str,
) -> Result<serde_json::Value, String> {
    let parts: Vec<&str> = spec.split(',').collect();
    if parts.len() != 3 && parts.len() != 5 {
        return Err("--probe takes r,x,y or r,x,y,dx,dy".into());
    }
    let index: u32 = parts[0].parse().map_err(|_| "bad probe direction")?;
    if index >= cert.angle_count {
        return Err("probe direction must be a net index".into());
    }
    let numbers: Vec<f64> = parts[1..]
        .iter()
        .map(|p| {
            p.parse::<f64>()
                .map_err(|_| format!("bad probe number {p}"))
        })
        .collect::<Result<_, _>>()?;
    let (x, y) = (numbers[0], numbers[1]);
    let (c, s) = sqverify_fast::certificate::direction(&cert.step, index);
    let exact = sqverify_fast::oracle::coverage(
        cert,
        &sqverify_fast::exact::of_f64(x),
        &sqverify_fast::exact::of_f64(y),
        &c,
        &s,
    );
    let centre = sqverify_fast::rotated::centre_lower_bound(cert, index, x, y)?;
    let estimate = sqverify_fast::rotated::centre_estimate_up(cert, index, x, y)?;
    let mut out = json!({"r": index, "x": x, "y": y, "centre_lower_bound": centre, "centre_estimate_up": estimate, "exact_coverage": exact.to_string(),
        "exact_coverage_approx": num_traits::ToPrimitive::to_f64(&exact)});
    if numbers.len() == 4 {
        out["dx"] = json!(numbers[2]);
        out["dy"] = json!(numbers[3]);
        out["box_lower_bound"] = json!(sqverify_fast::rotated::box_lower_bound(
            cert, index, x, y, numbers[2], numbers[3]
        )?);
    }
    Ok(out)
}

fn main() -> ExitCode {
    match run() {
        Ok(true) => ExitCode::SUCCESS,
        Ok(false) => ExitCode::from(1),
        Err(message) => {
            eprintln!("sqverify-fast: {message}");
            ExitCode::from(2)
        }
    }
}

fn run() -> Result<bool, String> {
    let options = parse_args()?;
    let side = options.side.as_deref().map(parse_rational).transpose()?;
    let (raw, value) = read_json(&options.candidate).map_err(|e| e.to_string())?;
    let cert = admit(&raw, &value, options.n, side.as_ref()).map_err(|e| e.to_string())?;
    // The default threshold is the one the certificate declares, so verdicts
    // compare with its authors'; without a declaration it is 1, which the
    // packing bound needs.
    let threshold = match &options.threshold {
        Some(text) => parse_rational(text)?,
        None => cert
            .declared_threshold
            .clone()
            .unwrap_or_else(sqverify_fast::exact::one),
    };
    if threshold < sqverify_fast::exact::one() {
        return Err("the threshold must be at least 1".into());
    }
    if let Some(spec) = &options.probe {
        println!("{}", probe(&cert, spec)?);
        return Ok(true);
    }
    let directions = parse_directions(&options.directions, cert.angle_count)?;
    if let Some(dir) = &options.receipts {
        std::fs::create_dir_all(dir)
            .map_err(|e| format!("cannot create {}: {e}", dir.display()))?;
    }
    let started = std::time::Instant::now();
    let next = AtomicUsize::new(0);
    let reports = Mutex::new(Vec::new());
    let failure = Mutex::new(None);
    std::thread::scope(|scope| {
        for _ in 0..options.threads.min(directions.len()) {
            scope.spawn(|| {
                loop {
                    let position = next.fetch_add(1, Ordering::Relaxed);
                    let Some(&index) = directions.get(position) else {
                        break;
                    };
                    match run_direction(&cert, index, &threshold, options.limits, options.confirm) {
                        Ok(report) => {
                            println!("{}", report.receipt);
                            if let Ok(mut all) = reports.lock() {
                                all.push(report);
                            }
                        }
                        Err(message) => {
                            if let Ok(mut slot) = failure.lock() {
                                *slot = Some(message);
                            }
                            break;
                        }
                    }
                }
            });
        }
    });
    if let Some(message) = failure.into_inner().map_err(|_| "worker panicked")? {
        return Err(message);
    }
    let mut reports = reports.into_inner().map_err(|_| "worker panicked")?;
    reports.sort_by_key(|r| r.index);
    if let Some(dir) = &options.receipts {
        for report in &reports {
            let path = dir.join(format!("r{:03}.json", report.index));
            let mut receipt = report.receipt.clone();
            receipt["certificate_sha256"] = json!(cert.input_sha256);
            let text = serde_json::to_string_pretty(&receipt).map_err(|e| e.to_string())? + "\n";
            std::fs::write(&path, text)
                .map_err(|e| format!("cannot write {}: {e}", path.display()))?;
        }
    }
    let all_verified = reports.len() == directions.len() && reports.iter().all(|r| r.verified);
    let full_net = directions.len() == cert.angle_count as usize;
    let status = match (all_verified, full_net) {
        (true, true) => "VERIFIED",
        (true, false) => "PARTIAL",
        (false, _) => "REFUSED",
    };
    let summary = json!({
        "kind": "sqverify-fast-summary/v1",
        "status": status,
        "threshold": threshold.to_string(),
        "directions": directions.len(),
        "refused_directions": reports.iter().filter(|r| !r.verified).map(|r| r.index).collect::<Vec<_>>(),
        "nodes": reports.iter().map(|r| r.receipt["nodes"].as_u64().unwrap_or(0)).sum::<u64>(),
        "direction_seconds": reports.iter().map(|r| r.seconds).sum::<f64>(),
        "direction_cpu_seconds": reports.iter().filter_map(|r| r.receipt["cpu_seconds"].as_f64()).sum::<f64>(),
        "wall_seconds": started.elapsed().as_secs_f64(),
        "threads": options.threads,
        "build": sqverify_fast::build_identity(),
        "premises": premises(&cert),
        "fault_injected_at_box": options.limits.inject_fault_at,
    });
    println!("{summary}");
    if let Some(dir) = &options.receipts {
        let path = dir.join("summary.json");
        let text = serde_json::to_string_pretty(&summary).map_err(|e| e.to_string())? + "\n";
        std::fs::write(&path, text).map_err(|e| format!("cannot write {}: {e}", path.display()))?;
    }
    Ok(all_verified)
}
