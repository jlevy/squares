//! Command-line entry point for the native n17 certificate verifier.
#![forbid(unsafe_code)]
use n17_kernel_verifier::json;
use n17_kernel_verifier::{
    Result,
    exact::integer,
    malformed, pyjson,
    verify::{Options, cover_cells, file_cells, verify, write_receipt},
};
fn run() -> Result<i32> {
    let raw = std::env::args_os()
        .skip(1)
        .map(|s| {
            s.into_string()
                .map_err(|_| malformed("argument is not UTF-8"))
        })
        .collect::<Result<Vec<_>>>()?;
    let mut args = raw.into_iter();
    let mut positional_only = false;
    let mut directory = None;
    let mut output = None;
    let mut cells = None;
    let mut sha = None;
    let mut options = Options::default();
    while let Some(arg) = args.next() {
        if positional_only {
            if directory.replace(arg).is_some() {
                return Err(malformed("only one directory is allowed"));
            }
            continue;
        }
        if arg == "--" {
            positional_only = true;
            continue;
        }
        let (option, inline) = if arg.starts_with("--") {
            arg.split_once('=')
                .map_or((arg.as_str(), None), |(a, b)| (a, Some(b)))
        } else {
            (arg.as_str(), None)
        };
        match option {
            "-h" | "--help" => {
                println!(
                    "n17-kernel-verifier DIRECTORY --output RECEIPT [--cells FILE --cells-sha256 HEX] [--sample N] [--sample-seed S] [--progress] [--threads K]"
                );
                return Ok(0);
            }
            "--progress" if inline.is_none() => options.progress = true,
            "--output" | "--cells" | "--cells-sha256" | "--sample" | "--sample-seed"
            | "--threads" => {
                let value = inline
                    .map(str::to_owned)
                    .or_else(|| args.next())
                    .ok_or_else(|| malformed(format!("{option} needs a value")))?;
                match option {
                    "--output" => output = Some(value),
                    "--cells" => cells = Some(value),
                    "--cells-sha256" => sha = Some(value),
                    "--sample" => options.sample = Some(integer(&value)?),
                    "--sample-seed" => options.sample_seed = integer(&value)?,
                    "--threads" => {
                        options.threads = integer(&value)?
                            .to_usize()
                            .ok_or_else(|| malformed("invalid thread count"))?;
                        if options.threads == 0 {
                            return Err(malformed("--threads must be positive"));
                        }
                    }
                    _ => {}
                }
            }
            _ if arg.starts_with('-') => return Err(malformed(format!("unknown option {arg}"))),
            _ => {
                if directory.replace(arg).is_some() {
                    return Err(malformed("only one directory is allowed"));
                }
            }
        }
    }
    let directory = directory.ok_or_else(|| malformed("DIRECTORY is required"))?;
    let output = output.ok_or_else(|| malformed("--output is required"))?;
    let cells = if let Some(path) = cells {
        file_cells(
            &path,
            &sha.ok_or_else(|| malformed("--cells needs --cells-sha256"))?,
        )?
    } else {
        cover_cells()?
    };
    let receipt = verify(&directory, &cells, &options)?;
    write_receipt(std::path::Path::new(&output), &receipt)?;
    let summary = json!({"status":receipt["status"],"failure":receipt["failure"],"mode":receipt["mode"],"seconds":receipt["seconds"]});
    println!("{}", pyjson::compact(&summary)?);
    Ok(i32::from(receipt["status"] != "PASS"))
}
fn main() {
    match run() {
        Ok(code) => std::process::exit(code),
        Err(e) => {
            eprintln!("{e}");
            std::process::exit(1);
        }
    }
}
