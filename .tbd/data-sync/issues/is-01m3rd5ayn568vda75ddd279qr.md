---
type: is
id: is-01m3rd5ayn568vda75ddd279qr
title: "Exact mixed-cover checker: faster options, and what a re-run of identical code actually validates"
kind: feature
status: open
priority: 2
version: 4
labels:
  - packing
  - pipeline
  - research
  - efficiency
dependencies: []
created_at: 2026-09-30T05:38:53.517Z
updated_at: 2026-09-30T05:48:24.107Z
---
## Question

The exact mixed-cover checker behind `s(21) = 5` (T-052) and `s(45) = 7` (T-053) is slow. Should it be improved, and which improvement buys real validation rather than ceremony?

## What runs today and what it proves

Evan Daniel's covers are certified at margin zero by two checkers from the same source:

| Checker | Code | Arithmetic | Mixed covers? | Cost at the source | Replayed here |
| --- | --- | --- | --- | --- | --- |
| `zmx2` | Rust, `verify2/src/bin/zmx2.rs` | exact integer tests on outward-rounded binary64 enclosures | yes | seconds to minutes (full `s(21)` 198 s here) | in full, both covers, `--d4` and `--full` |
| `zm_mixed.py` | Python, with `mixed_cover.py` and `zeromargin.py`, about 3,500 lines | exact `fractions.Fraction` | yes | 12.9 and 16.5 CPU-hours | 64-root sample; the full re-sweep started 2026-09-30 05:24Z (`think-l6la`) runs at about 1.3 times the source's per-root CPU, about 9 to 10 hours on 2 workers per cover |
| `zmcheck` | Rust, `verify2/src/main.rs` in the 2026-09-26 packet | exact `i128` | **no**, points only | `s(32)`: 80.2 CPU-hours, 5 of 3,600 roots uncertified | no |

**The cost is mostly the lemmas, not the language.** `zmcheck` is exact native code, yet on the `s(32)` point cover it was about 30 times slower than `zeromargin.py` (2.8 CPU-hours), because its pruning lemmas are weaker. How many boxes a checker opens matters more than how fast it decides each one.

## What the running re-sweep validates, honestly

The re-sweep runs the source's own unchanged `zm_mixed.py` over every root and compares each root's census with the shipped record. The checker is deterministic and exact, and the 64-root sample already reproduced the source's census exactly. So a full re-run of identical code on identical input adds three things:

- the shipped records are complete;
- they came from this version of the code and are not stale after an edit;
- the result does not depend on the platform.

Those are real, but small, in a non-adversarial setting. Agreement of the same code with itself is not independent confirmation. The evidence that matters is agreement between checkers that are built differently: here, exact Python against float-enclosure Rust. The two were written by one author and one agent, and share the D4 fold and the point test.

## Hashing: what is ceremony here and what is not

Per `OR-16` and `tbd guidelines general-coding-rules` → Cryptographic Hash Checks:

- **Not a constraint.** `zm_mixed.py`'s resume header records the SHA-256 of its three source files and the cover, and `--resume` refuses a file with a different header. That stops one resumed run from mixing records written by two versions of the checker. It does not stop anyone improving the checker: a changed checker writes its own records file. "Changing the checker's bytes makes its resume check refuse" is not a reason to avoid improving it. The session that said so on 2026-09-30 was wrong.
- **Ceremony to remove.** `packing/devtools/audit_evand_mixed_covers.py` reports the SHA-256 of files that live in git: the `sha256`, `shipped_sha256` and `replays[].sha256` fields in its JSON. The same goes for each evand packet's `retained-files.sha256`. Git revision and path already identify those bytes, and development.md says not to add such fields. Drop the fields the next time the audit's receipt is regenerated, which happens when the `think-l6la` re-sweeps are recorded. Leave the existing packets' manifests as frozen evidence (`OR-16`), but add no new ones.
- **Legitimate, and named.** `header_sha256_match_retained_files` compares the digests the source's own run wrote into its records header with the checker files the source published. That value is independently supplied, and the check detects shipped records produced by a different version of the checker than the one shipped: stale records after an edit, which did happen between `ebf8bbc3` and `ee3e2915`. `header_sha256_equal` in `compare-zm-mixed` confirms that a replay ran the same checker version as the source, which is what makes a census difference meaningful. Keep both, and have the code name the boundary. Likewise, comparing a download with a value its publisher supplies independently is legitimate: for example, the SHA-256 the #247 authors published for their certificate, checked against the Zenodo download.

## Options

| | Option | Speed | Validation it buys | Cost and risk |
| --- | --- | --- | --- | --- |
| A | Let the running Python re-sweep finish | none (finishes about 15:00 to 16:00Z on 2026-09-30) | completes the rung the register's `next_rung` names for T-052 and T-053 (`C4`); small marginal validation, as above | CPU only; competes with the other lanes for 4 cores |
| B | Improve `zm_mixed.py` in place: profile, move hot paths from `Fraction` to scaled integers or `gmpy2.mpq`, and keep the lemmas and subdivision order | probably 3 to 10 times | faithfulness shown practically: every root's census must equal the 118,400 shipped records exactly | about half a day; small review, since the diff is local; our fork, credited to the source |
| C | Port `zm_mixed.py` to Rust with exact arithmetic (`i128` with checked overflow and a bigint fallback, or `num-rational`), keeping the lemmas and subdivision order | probably 20 to 100 times; a cover in minutes | the same census-equality control, plus a second language and arithmetic stack | 1 to 2 days with review; about 3,500 lines of careful mathematics; lives beside `packing/sqsearch` under the Rust floor |
| D | Write an independent exact checker from `search/ZM_MIXED.md`'s lemmas, not the code, possibly with stronger lemmas (for example `zmx2`'s pair lemma Z done exactly) | depends on the lemmas | the strongest evidence: a different author and different code, so agreement is real confirmation; its census will not match root for root, so it is validated by verdicts and its own review | several days; needs a full mathematical review; the one option that changes what `C4` rests on |
| E | Fan the existing checker out across cloud sessions by region slices (`--cx-lo/--cx-hi/--cy-lo/--cy-hi`; `compare-zm-mixed` already takes several record files; `zm-mixed` would need multi-file input) | linear in machines; about 2 to 3 hours on 4 extra sessions | the same as A | extra branches need the owner's OK; the 2026-09-29 attempt in two cloud sessions went idle and landed nothing |
| F | Extend `zmcheck` (exact `i128` Rust) to segments | unclear; weaker lemmas | a third checker from the source's own author | the least attractive: 80 CPU-hours on `s(32)` already |

## Recommendation

- Let A finish; it costs nothing but CPU overnight and closes `think-l6la`.
- Do B next time a cover of this kind arrives. It is cheap, and its acceptance test is exact.
- Take C only if the family keeps producing covers (the next `s(k² − 4)` case, `s(60) = 8`, or further point-plus-segment covers). Then 10 to 20 CPU-hours per cover limits iteration.
- Take D if the owner wants the equality results to rest on a checker this project wrote from the mathematics. That is the only option that changes the confirmation rather than the speed.
- Separately, remove the digest ceremony in `audit_evand_mixed_covers.py` and the packets.
- Owner question: should `epistemics.md` say that re-running identical deterministic code is a reproducibility check, not a second confirmation, so that `C4` asks for differently built checkers rather than full re-runs of shipped code? Today's rule is satisfied by A.

## Acceptance for B or C

Every one of the 40,000 (`s(21)`) and 78,400 (`s(45)`) D4 roots gives exactly the shipped census:
- the ADM, CORE, P1, MIX, CHAIN, TRI, PIECE, EMPTY, UNCERT, THR, LIN, TPTS and SPLIT counts;
- the box count and maximum depth.

Two mutated covers, weakened as `ZMX2_AUDIT.md` does, must be refused, and the per-cover wall time must be recorded. `devtools.audit_evand_mixed_covers compare-zm-mixed` already performs the census comparison.

## References

- Packets: `packing/resources/web/evand-square-packing-2026-09-26/` and `-2026-09-28/` (the 09-28 README, "Not Replayed Here, and What Each Would Take" and "Full `zm_mixed` Re-sweeps").
- Beads: `think-l6la` (the re-sweeps) and `think-jyf4` (the hash debt).
- Records: T-052, T-053, T-051.
