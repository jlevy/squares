# Mykhailo Polkovskyi’s KKT Refinements at 70a033f

[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/70a033f0ecfa9e643cd5fb5dbac190cb7f4ffb94/certificates)
at `70a033f0ecfa9e643cd5fb5dbac190cb7f4ffb94` (tree
`c816b6f977f91a64068353ce7d39770a73e1e2f5`, committed 2026-10-14T16:11:31Z) replaces 24
of the 73 certificates [issue #593](https://github.com/jlevy/squares/issues/593) reported
at `46f638c` ([the #593 packet](../mishapolk-records-2026-10-14/README.md)).
No issue reports the commit. The record reads it as a publication in a watched
repository, reported at its first commit (the owner, 14 October 2026), and the 14 October
intake triaged it under bead `think-o644`.
The commit is seven past #593’s pin; the six between change only `ISSUE_REGISTRATION.md`,
the issue’s draft. It was still the branch head when the source was retrieved, at
2026-10-14T22:31Z.

The commit message reads “Refine 14 contested certificates to ultra-precision KKT
endpoints: strictly defeat PingYou PR #574, Couzo #583, #586, and Ostashev #575”.
It changes `certificates/census.json`, the 24 certificates `certificates/n<n>.cert` at n
= 129, 153, 154, 155, 156, 175, 176, 181, 204, 207, 209, 232, 264, 267, 270, 271, 272,
302, 303, 304, 305, 306, 307 and 308, and the 14 copies `certificates/square-<n>.cert` at
the 14 counts the message names, each byte-identical to `n<n>.cert`.
The census credits those 14 to “Mykhailo Polkovskyi (ultra-precision KKT dual-verified
optimum)” and the other 10 to “Antigravity (high-precision dual-verified contact
optimum)”.
Every one of the 24 files was first committed in `70a033f`, and none is byte-identical to
a file any packet here retains.

**Measured against the record at `main` `9b32da04d` and every earlier report, the
certificate is below every report at 12 counts: 129, 154, 156, 175, 176, 204, 232, 264,
271, 302, 303 and 304.** At each of those it tightens the certificate that held the
count, by $1.25 \times 10^{-94}$ (176) to $1.79 \times 10^{-19}$ (302 and 304), placing
every square where that certificate does to within $1.1 \times 10^{-3}$.
At the other 12, PingYou Ltd’s PR #574 (`T-174`) is smaller: by $1.49 \times 10^{-99}$ at
207, decided here exactly against PR #574’s algebraic side, by $1.29 \times 10^{-39}$ at
153, and by $1.30$ to $1.80 \times 10^{-23}$ at the ten “Antigravity” counts.

## Source Custody

The tree has no licence file and its README states no reuse terms.
Under the derived-only form of the
[existing retention policy](../known-best-packings/README.md), as for the
[#593 packet](../mishapolk-records-2026-10-14/README.md), this packet keeps no upstream
byte. No redistribution permission or licence determination is asserted.

`devtools.acquire_source` wrote the packet from a blobless clone checked out at the pin,
from the declaration in [acquisition/declaration.json](acquisition/declaration.json).
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
The declared scope is 40 files, 2,979,882 bytes, all pinned only: the README (SHA-256
`d1b8a7da7c0e61e38ce558bedc54ca0429bdce7ef9bf1778890852b8e13c6378`, the same bytes as
at `46f638c`), `certificates/census.json` and the 38 changed certificate files.
The declared `source/` directory is empty by design.

## Derived Facts

`devtools.upper_bound_reports derive` read the 24 certificates from the checkout at the
pin, after `devtools.acquire_source` showed that the checkout yields this packet’s
acquisition record and manifest, so the bytes it read have the digests the manifest
records. It wrote each as an exact rational `center-basis` Witness/v2 under `facts/`,
naming the certificate’s SHA-256 as `revision_sha256`; `derive --check` compares them
with the checkout again. Offline each fact must rebuild itself from the certificate it
states.

The census states each count’s exact `side_fraction`, and every certificate’s header
equals it, so each is admitted there (`printed_in` in
[acquisition/report.json](acquisition/report.json)); its `side_float` is a binary64
rendering and is not read.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record at `main` `9b32da04d` (14 October 2026, after #602 registered `T-161` to `T-184`),
and `check-claims` rebuilds it: each case ceiling from its holder’s own packet, each
register entry at the count from its own packet or, where it has none, from the bound its
claim states, and each other report from its own packet.
The houses are #593’s: no case record’s upper lanes have moved at these counts since.
Beside them stand every report #593’s packet compared with, each under the `T-NNN` #602
gave it where it has one; #593’s own certificate at `46f638c`; Francisco Couzo’s 175 at
`337078c`, which #506 does not name and its author asked on 14 October to import; and
Kevin Fang’s `T-163` at 307.
On 15 October, at reviews A6, B2 and B3 of #612, the declaration gained the registered
reports that list left out: `T-136` at 154 and 232, `T-140` at 175, `T-101` at 264,
#488’s unnamed 303 and `T-056`’s printed sides at 154, 156, 271, 302, 303 and 304. Its
labels now name Couzo’s 175 as `T-185` and `T-130` by PR #460, and the claim record was
frozen again; no verdict moved.
At 153, 207 and 302, PR #574’s sides are algebraic numbers, and the comparison reads them
exactly from that packet’s derived field witnesses (`facts/alg-n-NNN.yaml.gz` in
[the PR #574 packet](../pingyou-pr574-certificates-2026-10-13/README.md)): the relation
by the exact sign of the difference in the side’s number field, and the margin from an
enclosure refined until it excludes the certificate’s side.

| n | Side, rounded up at 16 places | Against the case’s exact ceiling | Nearest other report | Smallest |
| --- | --- | --- | --- | --- |
| 129 | 11.8700138504044644 | below by $2.02 \times 10^{-3}$ (Ryan Xu, improved by Evan Daniel, T-146) | below T-174 (PR #574) by $1.10 \times 10^{-21}$ | this certificate |
| 153 | 12.8700138504044644 | below by $2.58 \times 10^{-12}$ (PingYou Ltd, T-148) | above T-174 (PR #574) by $1.29 \times 10^{-39}$ | T-174 (PR #574) |
| 154 | 12.9212065771326311 | below by $1.36 \times 10^{-3}$ (Evan Daniel, T-160) | below T-182 (#586) by $1.29 \times 10^{-19}$ | this certificate |
| 155 | 12.9524254069584562 | below by $1.30 \times 10^{-19}$ (Daniil Ostashev, T-149) | above T-174 (PR #574) by $1.30 \times 10^{-23}$ | T-174 (PR #574) |
| 156 | 12.9791658538342765 | below by $6.76 \times 10^{-6}$ (Daniil Ostashev, T-149) | below T-174 (PR #574) by $1.19 \times 10^{-34}$ | this certificate |
| 175 | 13.7641743174865967 | below by $1.38 \times 10^{-19}$ (Daniil Ostashev, T-158) | below T-174 (PR #574) by $7.23 \times 10^{-75}$ | this certificate |
| 176 | 13.7958723184364073 | below by $1.70 \times 10^{-2}$ (Nate Chaoweeraprasit (itsnaka), T-151) | below T-174 (PR #574) by $1.25 \times 10^{-94}$ | this certificate |
| 181 | 13.9508195310229241 | above by $1.40 \times 10^{-23}$ (Nate Chaoweeraprasit (itsnaka), T-151) | above T-174 (PR #574) by $1.40 \times 10^{-23}$ | T-174 (PR #574) |
| 204 | 14.8086632343869566 | below by $1.42 \times 10^{-2}$ (the Kingbird catalogue, verified by Evan Daniel's exact ceiling, T-101) | below T-174 (PR #574) by $1.83 \times 10^{-21}$ | this certificate |
| 207 | 14.8809603715555796 | below by $1.49 \times 10^{-9}$ (PingYou Ltd, T-147) | above T-174 (PR #574) by $1.49 \times 10^{-99}$ | T-174 (PR #574) |
| 209 | 14.9462232264464511 | below by $1.49 \times 10^{-19}$ (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-140) | above T-174 (PR #574) by $1.49 \times 10^{-23}$ | T-174 (PR #574) |
| 232 | 15.7641743174865967 | below by $1.58 \times 10^{-19}$ (Daniil Ostashev, T-158) | below T-174 (PR #574) by $1.45 \times 10^{-74}$ | this certificate |
| 264 | 16.7747351323878329 | below by $1.68 \times 10^{-19}$ (Daniil Ostashev, T-158) | below T-174 (PR #574) by $1.75 \times 10^{-74}$ | this certificate |
| 267 | 16.8388152699482623 | below by $1.68 \times 10^{-19}$ (Ryan Xu, improved by Francisco Couzo, T-134) | above T-174 (PR #574) by $1.68 \times 10^{-23}$ | T-174 (PR #574) |
| 270 | 16.9281969933290166 | above by $1.69 \times 10^{-23}$ (Nate Chaoweeraprasit (itsnaka), T-151) | above T-174 (PR #574) by $1.69 \times 10^{-23}$ | T-174 (PR #574) |
| 271 | 16.9489923564512057 | below by $1.24 \times 10^{-4}$ (Nate Chaoweeraprasit (itsnaka), T-151) | below T-174 (PR #574) by $2.09 \times 10^{-34}$ | this certificate |
| 272 | 16.9655864748376707 | below by $5.26 \times 10^{-16}$ (Nate Chaoweeraprasit (itsnaka), T-151) | above T-171 (#569) by $1.70 \times 10^{-23}$ | T-174 (PR #574) |
| 302 | 17.8700138504044644 | below by $2.02 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | below T-181 (#583, #586) by $1.79 \times 10^{-19}$ | this certificate |
| 303 | 17.9099582910699080 | below by $3.11 \times 10^{-3}$ (Nate Chaoweeraprasit (itsnaka), improved by Evan Daniel, T-146) | below T-174 (PR #574) by $2.43 \times 10^{-74}$ | this certificate |
| 304 | 17.9294277580751750 | below by $1.38 \times 10^{-4}$ (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-152) | below T-175 (#575) by $1.79 \times 10^{-19}$ | this certificate |
| 305 | 17.9504664821377123 | below by $1.79 \times 10^{-19}$ (Nate Chaoweeraprasit (itsnaka), improved by Francisco Couzo, T-152) | above T-174 (PR #574) by $1.80 \times 10^{-23}$ | T-174 (PR #574) |
| 306 | 17.9634337174914258 | below by $1.80 \times 10^{-19}$ (Francisco Couzo, T-128) | above T-174 (PR #574) by $1.80 \times 10^{-23}$ | T-174 (PR #574) |
| 307 | 17.9808627840546911 | above by $1.80 \times 10^{-23}$ (Nate Chaoweeraprasit (itsnaka), T-136) | above T-174 (PR #574) by $1.80 \times 10^{-23}$ | T-174 (PR #574) |
| 308 | 17.9982698795262559 | below by $1.80 \times 10^{-19}$ (Kevin Fang, improved by Evan Daniel, T-141) | above T-174 (PR #574) by $1.80 \times 10^{-23}$ | T-174 (PR #574) |

**207.** The 14 October triage left 207 undecided: the certificate’s side,
`1488096037155557959469669157492336415899451456818029930847400016655137842386538704278321841865696320894963008089/10^110`,
is $1.46 \times 10^{-41}$ above PR #574’s 40-place print. PR #574’s side is
$1288/89 + (209/178)b - (78/89)b^2 + (335/178)b^3 - (12/89)b^4$, $b \approx 0.3714$ the
root of $b^5 - 14b^4 + 6b^3 + 4b^2 - 7b + 2$ in its retained isolating interval.
The exact sign of their difference puts PR #574’s side below the certificate’s by
$1.49 \times 10^{-99}$ (`difference_bounds` in the claim record), so the certificate is
PR #574’s side rounded up near the 99th place, and 207 is not recorded.

## Report Order and Lineage

The owner’s rule of 14 October takes the reports at each count in the order they reached
the record and records one only where it is decidably below every earlier report and the
record. `70a033f`, at 2026-10-14T16:11:31Z, is later than every report the
[14 October ledger](../../../campaign/issue-intake/upper-bounds-20261014/README.md)
walks at these counts, and no report at these counts reached the record between the
ledger’s read and it: no issue or comment states a bound at them, PR #574’s head is still
`4c319c2`, and no watched repository published one (Ostashev’s head `b909e1b` is of 12
October; Couzo’s `487b058` and `43ac7d2`, later on 14 October, add no certificate at
these counts). Issue #606, later the same evening, is at 146 only.
So the claim record’s verdict is the rule’s: **recorded at 129, 154, 156, 175, 176, 204,
232, 264, 271, 302, 303 and 304; not recorded at the other twelve**, PR #574 being
decidably smaller at each.

At every recorded count the certificate tightens the certificate that held the count.
[review/compare_lineage.py](review/compare_lineage.py) matches its square centres,
greedily and nearest first under the box’s 8 symmetries, with each holder’s certificate
read from its own packet
([review/compare_lineage-output.txt](review/compare_lineage-output.txt)):

| n | Certificate it tightens | Packing first found by | Centres within 1e-6 | Largest centre distance |
| --- | --- | --- | --- | --- |
| 129 | PR #574 (`T-174`) | Daniil Ostashev (#562, `T-162`) | 127 of 129 | $1.4 \times 10^{-4}$ |
| 154 | #586 (`T-182`) | Francisco Couzo | 144 of 154 | $6.4 \times 10^{-4}$ |
| 156 | PR #574 (`T-174`) | Francisco Couzo (#561, `T-161`) | 156 of 156 | $7.6 \times 10^{-16}$ |
| 175 | PR #574 (`T-174`) | Daniil Ostashev (#528, `T-158`) | 175 of 175 | $9.2 \times 10^{-16}$ |
| 176 | PR #574 (`T-174`) | Daniil Ostashev (#575) | 159 of 176 | $1.4 \times 10^{-4}$ |
| 204 | PR #574 (`T-174`) | Daniil Ostashev (#562, `T-162`) | 192 of 204 | $1.0 \times 10^{-3}$ |
| 232 | PR #574 (`T-174`) | Daniil Ostashev (#528, `T-158`) | 147 of 232 | $2.8 \times 10^{-4}$ |
| 264 | PR #574 (`T-174`) | Daniil Ostashev (#528, `T-158`) | 264 of 264 | $1.2 \times 10^{-15}$ |
| 271 | PR #574 (`T-174`) | Francisco Couzo (#561, `T-161`) | 271 of 271 | $9.9 \times 10^{-16}$ |
| 302 | #583 and #586 (`T-181`) | Francisco Couzo | 302 of 302 | $7.8 \times 10^{-16}$ |
| 303 | PR #574 (`T-174`) | Daniil Ostashev (#562, `T-162`) | 303 of 303 | $9.5 \times 10^{-16}$ |
| 304 | #575 (`T-175`) | Daniil Ostashev | 304 of 304 | $9.4 \times 10^{-16}$ |

The first-found column is the 14 October ledger’s account of whose packing PR #574
refines at each count; PR #574’s own lineage is its claim.
At 129, 154, 176, 204 and 232 some centres move by more than $10^{-6}$, as many as 85 of
232, but none by more than $1.1 \times 10^{-3}$; at the other seven every centre stays
within $1.3 \times 10^{-15}$.
Each reads as the same arrangement re-solved, a refinement in the ledger’s sense, to be
credited to its finder after the finder of the packing it refines, as a regularization
([result-import.md](../../../campaign/result-import.md#several-reports-at-one-count)).
The measurement decides nothing.

## Exact Replay

Only the facts enter geometry decisions, through the maintained two-route kernel of
`devtools.evand_arrangement_reports`: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion.
All 24 certificates were replayed, the twelve the rule records and the twelve it does
not, each with a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on one worker.

All 24 positives pass both routes, and both routes refuse all 48 controls, each on the
overlap or the wall it was built to break.
In every positive the two routes find the same least wall clearance and the same least
pair gap, the pair gap twice the wall clearance, which a contact point scaled by a small
guard leaves: $5 \times 10^{-25}$ at the ten “Antigravity” counts; $5 \times 10^{-41}$ at
129, 153, 154, 156, 302 and 304; $5 \times 10^{-101}$ at 204, 207, 232, 264, 271 and 303;
$3.63 \times 10^{-78}$ at 175 and $3.62 \times 10^{-98}$ at 176.
No square touches a wall or another square.
The 72 jobs made 4,186,086 pair decisions in 2,167.90 route CPU seconds and 2,194.11 job
wall seconds, summed; the longest job took 78.28 seconds.
`certify --workers 1` took 37 minutes 36 seconds of wall time, 22:53:02Z to 23:30:38Z on
14 October, at a load average of 2 to 2.5 on four cores shared with another lane’s
replay. A fresh serial `check --replay` decided all 72 jobs again, equal to the retained
rows apart from timing, in 37 minutes 46 seconds, 23:31:19Z to 00:09:05Z, at a load
average of 2 to 8.
The receipts are one per count, `receipts/exact-certification-nNNN.json.xz`, since the
whole would exceed the kernel’s ceiling on uncompressed evidence; together they keep every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the source’s code. The third exact route
(`devtools.check_half_angle_area`) has not read these certificates: it needs a roster line
and a reader for this packet, and at the issue-552 import’s rate of about 41 seconds a
count with its six controls it would take about 20 minutes of one worker for the 24.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
“Ultra-precision KKT endpoints” and “dual-verified” are the source’s words; no KKT,
local-minimum or rigidity statement was checked here, and novelty, local or global
optimality and rigidity are not established.
The source’s README claims dual exact verification with Evan Daniel’s `verify_cert.py`
and `verify_cert2.py`; neither ran here, and no copy of either is in the pinned tree.

## Credit

On issue #593 (comment of 2026-10-14T15:38Z, repeating one of 15:16Z) the author asks
that all entries be credited to **Mykhailo Polkovskyi** (GitHub: @Mishapolk).
The census at the pin credits 14 counts to “Mykhailo Polkovskyi” and 10 to “Antigravity”,
and the commit names no co-author. The repository’s README and the #593 draft
(`ISSUE_REGISTRATION.md`, unchanged since `ec87dc6`) credit “Mishapolk (Mikhail Polk)”,
and the draft says: “Gemini 3.8 assisted with solver scripting, precision checks, and
formatting.” This packet records the census’s attribution as the source gives it and
does not read “Antigravity” as a person.
The twelve recorded counts are all among the census’s 14 Polkovskyi counts.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source mishapolk-kkt-refinements-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-kkt-refinements-2026-10-14 derive --checkout CHECKOUT --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-kkt-refinements-2026-10-14 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports mishapolk-kkt-refinements-2026-10-14 check --replay
uv run --frozen --all-extras --group dev python resources/web/mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py
```

`CHECKOUT` is a clone of the source at the pin. `check` admits the receipt structurally;
only `--replay` decides the geometry again. `register-plan` prints the record entries the
import needs, over the twelve recorded counts; [register-plan.yaml](register-plan.yaml)
keeps that output as it printed on 15 October 2026 at `main` `9b32da04d`, for the records
pull request. It writes no `regularizations`, which the records pull request adds, one per
count, naming the entry whose certificate each tightens (the table above), and its
sentence on “further certificates the issue does not name” stands for the twelve the rule
does not record: no issue reports this commit.
The records pull request of 15 October registers the twelve as `T-186`, at V0/C0, with
those twelve `regularizations` on the measured basis of
[review/compare_lineage-output.txt](review/compare_lineage-output.txt), says plainly that
the other twelve are not recorded, and credits Mykhailo Polkovskyi alone.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `facts/n-129.yaml.gz` | receipt | `1a752b021b8c24de2f22ed959d15e03fd5309816` | `84b8247b80ecba6afe3c8392129384b609e29857f20514fdb7872635e6daae4d` |
| `facts/n-153.yaml.gz` | receipt | `8337f1e47e00aa9c182efd041192ff27cceae584` | `f2f6f556df261cab1308d06de73a7e2406bef08e7fa45cdb700647168ea3433e` |
| `facts/n-154.yaml.gz` | receipt | `59ed1392baf07b2e28025bea390f201170ea5138` | `04f234d9dfba947ec455078495189de6421e6dfa43c76f11859a3dc66b62ddc9` |
| `facts/n-155.yaml.gz` | receipt | `5e918df322a117e1629bb8ca0fb73247b0f1da27` | `61219af0a6809bf63fd4ea7cc3f316558ca3483b96b0c4c876a1d7d490f1d267` |
| `facts/n-156.yaml.gz` | receipt | `1d46157229c8cf8dcd5858526d0bb65945f21c4d` | `82b77676c092e13d35f525b5fdb714e4104e67d62e5eaef62af0f470cabdc274` |
| `facts/n-175.yaml.gz` | receipt | `7bdc7b9a33b41b1599f76e16dd18128c7f351a31` | `f02c2aa4d2efc03d12b22769dd95c81a95329bfd98516be2330e469c455377b7` |
| `facts/n-176.yaml.gz` | receipt | `fb61766675c7b28b48ce049603cdcd966679317f` | `90f91cd78a53923cd60d99b26e79fc530be6f056e68ea1225dafd17a6d2b0b3a` |
| `facts/n-181.yaml.gz` | receipt | `3bcca6a0ad8456a1054605e89736aabd646e9bb7` | `4ab93fdb81f6813f9149e83f085d8a35b56bef138db9631b1174b860861ad8bf` |
| `facts/n-204.yaml.gz` | receipt | `46a3f53f07b4df521b5688bb83185be05c56d41a` | `ddce50d641febf10f7d0017e505c20296cc00afbe982236397f4270af08ba312` |
| `facts/n-207.yaml.gz` | receipt | `64b87b1e3c33ce56558a16c5f1f15aa03735ee59` | `2c92bf927616e1833d2064781324764b894cb35f746ef27d7eaf946ba1a217e0` |
| `facts/n-209.yaml.gz` | receipt | `c0ff394c69fbb96ec166b689f367ac24be08607c` | `94b6132301b1bff8cf420a8c48b4c94306578a500d27c5278b75e7cc5495eaa6` |
| `facts/n-232.yaml.gz` | receipt | `bd3dadf23b557fd4394c9390253798b4fd29e0ac` | `46c2bc08f6490648e5cf95fa6a77b2e399fca87893db1e962f6fa9381905ffe1` |
| `facts/n-264.yaml.gz` | receipt | `50c374d13c08525dc233edffb70f527e2e31aeed` | `ec44fd62259edbb24b4b10af16c36267bbc40f6de4d15f6c54f12ee37fb62572` |
| `facts/n-267.yaml.gz` | receipt | `5b3b7aed45e81cca26c93cd3b552fc9284e74123` | `15664a77afcc4dfd1f98c6fd9ac5adc6815efaa64bf03cf020bd1caadc5b1e71` |
| `facts/n-270.yaml.gz` | receipt | `9b1cae87ffcf54d488556860e41d7c0c9e48e38e` | `b58fe629c7aa43a3938a896d3a4fe1c1b4c97863f347891599d9ca0f4be4428e` |
| `facts/n-271.yaml.gz` | receipt | `0fee5ed34f6d99df338f7052e2ef395796c3293e` | `ba6c2370d613e5b0324c53503720223d1640f358cf8f37c33583e65c819fe6da` |
| `facts/n-272.yaml.gz` | receipt | `6e2b30ab2ae199f8f229cecbd0db9b92b2386408` | `171dbe7d141c9ef2e5eecd74dca2a07d51f06288edb54e7417581d02dadb91f4` |
| `facts/n-302.yaml.gz` | receipt | `87edd7857e036f75ce8232d6f51abb6072c1b984` | `8d1522a929a2415e863200e81a276a3097bbea2d9b670e8bced9ad6a9dd281c3` |
| `facts/n-303.yaml.gz` | receipt | `952c30180603f80ad8bb2894f71a2a4a9c92561a` | `c74f59e7732f37c9f7c5e82901e01556a835d4c9e8a7e726b6e7e75e57314a1c` |
| `facts/n-304.yaml.gz` | receipt | `05ca03b7f2c127bc7a11cc3336066555a0b9e72f` | `9b14863485c7186e0e25382fc0e73f0c354fbc05d3392db26b41f26651855829` |
| `facts/n-305.yaml.gz` | receipt | `087bc3edb131a4267a594cca64ee35e578c29418` | `e8eab7c7e6f54237547fe7888ddea7f8f3d040c79f9b83ee1b6cf7b1c2c7d601` |
| `facts/n-306.yaml.gz` | receipt | `4b94f2102539181befe7ddfaa38236f9b2c95fdd` | `026b176170cdae6112ca0024a8716aeef8d255771f9325b5c46434f465dfe0f3` |
| `facts/n-307.yaml.gz` | receipt | `2b592638f07308c143cebf36450381df9876febe` | `380a27ede75db823c3762a20990331530e71a0e3702e80b80f193ce85b8fb720` |
| `facts/n-308.yaml.gz` | receipt | `b03b8767f75a7f48b3e734e183998abb74c63203` | `31dc7020d18be0d802312cb046582489717c935f0a377fe87fa280edf164e478` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
