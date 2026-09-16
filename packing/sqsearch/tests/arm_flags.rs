//! Verify that sqsearch refuses arm flags that would run something other than they say.

use std::process::Command;

fn run(extra: &[&str]) -> std::process::Output {
    let mut args = vec![
        "--n",
        "4",
        "--chains",
        "1",
        "--threads",
        "1",
        "--steps",
        "3",
        "--max-restarts",
        "1",
        "--budget-moves",
        "3",
    ];
    args.extend_from_slice(extra);
    Command::new(env!("CARGO_BIN_EXE_sqsearch"))
        .args(&args)
        .output()
        .expect("run sqsearch")
}

#[test]
fn arm_flags_that_would_mislabel_the_run_are_refused() {
    let refused: [&[&str]; 7] = [
        // Pressure is on only when both ends of its ramp are positive, so one end alone
        // would run the control under a pressure label.
        &["--mu0", "0.05"],
        &["--mu1", "1e-6"],
        &["--mu0", "inf", "--mu1", "inf"],
        &["--mu0", "-1", "--mu1", "-1"],
        &["--p-perturb", "NaN"],
        &["--p-perturb", "1.5"],
        &["--p-perturb", "0.2", "--perturb-scale", "inf"],
    ];
    for flags in refused {
        let output = run(flags);
        assert!(
            !output.status.success(),
            "sqsearch accepted {flags:?}: {}",
            String::from_utf8_lossy(&output.stdout)
        );
        assert!(
            String::from_utf8_lossy(&output.stderr).contains("sqsearch: "),
            "no reason printed for {flags:?}"
        );
    }
    for flags in [
        &[][..],
        &["--mu0", "0.05", "--mu1", "1e-6"][..],
        &["--p-perturb", "0.2", "--perturb-scale", "1"][..],
    ] {
        let output = run(flags);
        assert!(
            output.status.success(),
            "sqsearch refused {flags:?}: {}",
            String::from_utf8_lossy(&output.stderr)
        );
    }
}

#[test]
fn basin_entry_refuses_the_same_flags() {
    let seed_path = std::path::Path::new(env!("CARGO_TARGET_TMPDIR"))
        .join(format!("sqsearch-arm-flags-{}.json", std::process::id()));
    std::fs::write(
        &seed_path,
        r#"{"x":[0.5,1.5,0.5,1.5],"y":[0.5,0.5,1.5,1.5],"t":[0,0,0,0]}"#,
    )
    .expect("write seed fixture");
    let output = Command::new(env!("CARGO_BIN_EXE_sqsearch"))
        .args([
            "--basin-entry",
            "--seed-config",
            seed_path.to_str().expect("utf-8 path"),
            "--trials",
            "1",
            "--eps",
            "0",
            "--steps",
            "3",
            "--budget-moves",
            "3",
            "--mu0",
            "0.05",
        ])
        .output()
        .expect("run sqsearch");
    let _ = std::fs::remove_file(&seed_path);
    assert!(!output.status.success(), "basin entry accepted --mu0 alone");
}
