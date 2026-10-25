VERIFIED N12 SOURCE AND COMPILED ARTIFACTS

The theorem is N12Compact.Final.optimality : S12.packingConstant12 = 4,
with unrestricted orientations/translations and disjoint interiors; contact
at boundaries is allowed. The complete lower bound and an attaining grid
are connected to the original packing constant.

SUCCESSFUL FINAL AUDIT
Repository EvolvingPrograms/SquaresLean, branch main,
source SHA 1f60d412707aae824b76fbaf11d4e708695451fa.
Run 38849916588, job 116808701733, attempt 1 succeeded. All 5,377 project
modules were reused after source/dependency/compiler/object/log receipt checks.
A fresh final check of the exact theorem type and axioms followed.

The final report is github-replay.json (global_optimality_proved=true).
The original ZIP also contains latest-replay.json, whose global flag is false:
that file describes module replay before the separate final audit. The final
report and global-type-axiom-audit.log are the authoritative final-stage records.
Old unrelated compiler logs may be present in the original ZIP; the accepted
receipt index selects the 5,377 logs belonging to this final proof.

Axiom audit: 3 standard axioms plus 1,624 approved native-generated axioms,
no sorryAx or unexpected custom axioms. The numerical classification inherits
native_decide compiler trust; this is not a kernel-only computational replay.
The current publication did not independently recompile the theorem.

RELEASE ASSETS
N12-jatloe-final-evidence-1.zip
  Original successful-run artifact12024837592; 2,934,549bytes.
  SHA256 db3447b212544e83028fdabd73cf3acd14b796e7ff977cbb899b6e7164b5d9f8
  Compiler logs, receipts, final report and audits; no compiled binaries.

N12-jatloe-compiled-checkpoint-38847898861.zip
  Original checkpoint artifact12023379882; 1,033,472,991bytes.
  SHA256 7a20bbdfc76a6f066dc6795e3c50b38c81641c5e99d4dff47536cc6fc1772496
  ZIP contains checkpoint.tar (3,072,215,040bytes), including:
  5,377 .olean files, 5,377 compiler logs, the receipt index and metadata.
  Project objects are Linux X64, using Lean4.35.0. No external libraries or
  compiler executables are included. Project files use the legacy Lean module
  format, so these objects do not require new-format .olean sidecars.

The checkpoint was saved by an earlier run,38847898861, at437041a0f00f1ff9166e46b1f7fc93942a441681.
That run failed later. Its saved objects were subsequently accepted by the
successful run above. Every object, source and compiler-log hash has been
checked against the later successful-run receipt index. Receipt JSON records
are identical despite different JSON serialization. No earlier run conclusion
is substituted for the successful final audit.

compiled-checkpoint-verification.json records this archive audit. It streamed
the nested tar without extracting it or invoking Lean. All expected members,
sizes and hashes matched. verified-source-manifest.json binds the 5,377 source
modules to the accepted source commit. All 5,462 tracked project Lean files,
including files outside the final closure, are preserved byte-for-byte.

REPRODUCE THE PRESERVATION CHECK (NO LEAN BUILD)
From repository root, with both ZIPs downloaded from the release:
  unzip N12-jatloe-final-evidence-1.zip -d /tmp/n12-successful-evidence
  python3 verification/run-38849916588/check_compiled_checkpoint.py \
    --archive N12-jatloe-compiled-checkpoint-38847898861.zip \
    --evidence /tmp/n12-successful-evidence \
    --project Lean/Proofs/N12-jatloe \
    --report /tmp/n12-object-check.json
The checker pins both original ZIP/receipt provenance and the successful final
report hash, validates all source/object/log correspondences, and does not
extract the large nested archive. This checks preservation, not proof validity
independently of the trusted original compiler and final audit.

FOR A FRESH LEAN REPLAY
Use the public manual workflow described in the root README, target N12-jatloe,
branch main. The project lock pins Lean4.35.0 and Mathlib56a005855ea17e0b0958f73ec801ae140b0a1679.
Its full cache and build-artifact uploads preserve compiler outputs for future
runs. Public workflow changes passed offline tests and have not themselves
been run end to end as part of this publication.
