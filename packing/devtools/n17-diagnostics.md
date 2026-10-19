# Retained n17 diagnostics

These opt-in tools inspect finite binary abstractions and fixed witness samples.
They do not admit exclusions, certify common poses or establish global optimality.
Search failure and missing known support remain unknown.
A producer receipt is distinct from independent verification.

The shared `bounded_diagnostics` helper checks the monotonic deadline and current worker
RSS. `process_memory.peak_memory_bytes` reports the lifetime high-water mark separately;
an earlier allocation does not permanently poison a reusable worker’s guard.
Current RSS is supported and tested on Windows, Linux and macOS. The macOS sampler reads
native `proc_pidinfo(PROC_PIDTASKINFO)` resident bytes and refuses failed or incomplete
responses. Its controls compare a live sample with `ps` and release a mapped allocation
to distinguish current RSS from the lifetime peak.
Other platforms refuse the sampler explicitly.
The external supervisor still provides whole-process-tree cleanup and its own limits.

Saved seed and node objects use semantic content digests because they are external
inputs. A cold receipt must attest the same objects and a stalled state.
Its timing, host and other bookkeeping metadata do not change input identity.
Legacy packets with `cold_receipt_sha256` are accepted after checking the seed/node
identity.

Committed evidence is identified by its repository path and historical Git revision.
The revision is informational: replay does not fetch or require old Git objects.
The bounded fixture reader compares type-aware JSON content and independently checks
models, exact references, nonempty inventories and coverage.
Historical cross-receipt digests are bookkeeping, not reuse gates.
New headers report revision/path provenance.
Fresh verifiers check scientific content and report `packet_content_verified`.

Retained JSON is written with the repository’s `sqpack.retained_json` formatter.
The shared writer checks the actual UTF-8 LF bytes against the 4 MiB packet ceiling
before replacing a destination.
Formatting retained files changes no JSON content and does not rerun their measurements.
The formatter is main’s own module, `sqpack.retained_json`.

Run from `packing/` with the existing Python 3.14 environment.
On POSIX:

```sh
uv run --frozen --all-extras --group dev python -m devtools.probe_n17_raw_row_support \
  "$SAVED_OBJECTS" --checked-receipt "$COLD_RECEIPT" \
  --verify "$RETAINED_PACKET" --output "$NEW_REPLAY"
```

On Windows:

```powershell
$ProjectPython = (Resolve-Path '.venv/Scripts/python.exe').Path
& $ProjectPython -m devtools.probe_n17_raw_row_support $SavedObjects `
  --checked-receipt $ColdReceipt --verify $RetainedPacket --output $NewReplay
```

Supply existing saved objects, a valid cold receipt and a new output path.
The session READMEs identify the corresponding retained packets and scoped conclusions.
Original inputs, historical measurements and portable archives remain immutable.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
