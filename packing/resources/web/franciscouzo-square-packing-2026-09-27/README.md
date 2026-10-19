# Francisco Couzo’s `square-packing`, Retrieved 2026-09-29

This packet records
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing), which
reports 49 packings of unit squares in a square, for 49 counts from `n = 68` to `307`,
each smaller than the Kingbird catalogue fetched on 25 September 2026.
Its author opened [jlevy/squares#227](https://github.com/jlevy/squares/issues/227) on
2026-09-23 at 02:48 UTC, asking for the first two to be registered: “I found better
solutions with the help of Claude for the 102 and 103 problems”.
Its Frontier key is **[franciscouzo square-packing 2026-09-27]**, and the result is
registered as T-056.

Every one of the 49 is below both the side this project recorded before this intake and
the live catalogue of 29 September 2026, and every one certifies exactly here.

## Source and Pin

| Field | Value |
| --- | --- |
| Revision | `f3c5a529c255b546db18605702b8da298132309f`, tree `2ca0583ce143d1639ae2a8aef60be00bf8e26bba`, committed 2026-09-27T21:46:41Z |
| History | Twelve commits. The first eight, authored between 2026-09-23T01:35Z and 2026-09-24T10:28Z, were committed again on 2026-09-24 between 10:33 and 10:34 UTC; the last four carry one clock. Early files were named by side (`n102_s10.607902017700.txt`) and renamed on 2026-09-24 |
| Author | Francisco Couzo, read from the commit metadata: the repository has no LICENSE and its README names no author |
| Credit | The README names no prior work beyond the catalogue it compares against, so nothing is credited after the author. The repository itself states no AI assistance; its author said on issue #227 that he found the 102 and 103 packings “with the help of Claude” |
| Licence | None published |
| Retrieved | 2026-09-29, a full clone |
| Retained here | Derived facts and metadata only: [`facts/`](facts/), one Witness/v2 witness per count with the source’s centres and angles carried verbatim, and [`acquisition/sources.json.gz`](acquisition/sources.json.gz), which pins all 99 upstream files by SHA-256 and records each count’s commit history with every side it has printed |
| Not retained | The 49 `nNNN.txt` packing files, their 49 SVG renderings and the README, under the derived-only form of the [known-best retention policy](../known-best-packings/README.md): no raw asset is kept (`raw_asset_retained: false`) |

## The Claims

Each `nNNN.txt` gives `n` and the side `s` on two comment lines, then one line per square
with its centre and angle in radians, origin at the lower-left corner, each a binary64
value printed as a `%.17e` literal.
The side a case takes is the one its file prints, to fifteen decimals; the README’s
table prints the same sides to twelve.
The repository states no method, no feasibility tolerance and no checker.

The acquisition record keeps every side each count has printed, by both clocks.
Most counts improved over several commits: `n = 180`, for example, went from
`13.932235154395972` on 23 September to `13.927888140501693` on 27 September.

## Certified Here

`python -m devtools.upper_bound_packets certify` promotes each retained witness to an
exact rational packing, the source’s pose rounded to rationals
(`packing-witness promote --strategy robust-rational --max-side-increase 1e-9`, in
process), and decides every pair and every wall over `ℚ` twice: once in the promotion’s
exact separating-axis test, and once in `devtools.check_rational_witness_independent`,
which shares no code with it.
Every one of the 49 promoted at centre dilation 1, so each certificate is the author’s
packing and not a relabelled or dilated one, and the certificate’s side differs from the
printed side by less than `2.2e-15` either way.
The certificates are committed as deterministic gzip under
[`packing/witnesses/franciscouzo-2026/`](../../../witnesses/franciscouzo-2026/); `gunzip -k`
restores the YAML that `packing-witness verify` reads.
[`receipts/certification.json.gz`](receipts/certification.json.gz) records each one’s digests,
exact side, pair count and both verdicts.

The verified upper bound a case carries is the larger of the printed side and the
certified side rounded up at the printed fifteen decimals.
At 20 counts that is the printed side, and at 26 it is one unit of the fifteenth decimal
above it, which `bounds_agree_at_declared_precision` accepts as the same bound.
At **`n = 206, 259` and `305`** the rounded-up certificate sits 2, 3 and 2 units of the
fifteenth decimal above the printed side, beyond the one unit
`bounds_agree_at_declared_precision` allows, so those three case records carry the
certified value, a `replay-failure` conflict and a `mathematics` blocker, and the
printed side itself is not certified.
The source’s binary64 coordinates do not carry the digits to close those gaps.

Two negative controls on the `n = 68` certificate, its side cut by `1e-15` and square 31
moved by `1e-6`, are refused by both checkers:
[`receipts/negative-controls.json`](receipts/negative-controls.json).
[`receipts/live-catalogue-2026-09-29.json`](receipts/live-catalogue-2026-09-29.json)
records the live catalogue’s side at each count on 29 September 2026, read from a page
that is not retained; every printed side is below it.

Replay, from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_packets \
  check --replay --source franciscouzo-square-packing --workers 4
```

which regenerates every certificate from the facts, requires its bytes to equal the
committed one, and decides the committed one again with the independent checker.
It takes about half an hour on four workers; the per-case walls are in the receipt.

## Interval Route

`python -m devtools.upper_bound_intervals certify` decides each source's pose again, as printed. Nothing is rounded to rationals: the printed centres, each angle in the radians the facts declare, and its true cosine and sine are all enclosed.

**Arithmetic.** It works in decimal fixed-point intervals of 40 digits rounded outward. Cosine and sine come from Taylor polynomials widened by the Lagrange remainder.

**Pairs.** 1,205,911 of the 1,229,925 pairs are separated by bounding circles, decided exactly on the printed centres. The other 24,014 are separated by the separating-axis test over the four edge normals. None needed more than 40 digits, and none touches. The least gap is `1.98e-13`, at `n = 106`.

**Side.** The side is the pose's own extent, enclosed to within `1e-39`, and the walls are checked on the translated pose.

**Independence.** The tool shares no geometry code with either exact checker, and takes nothing from `sqpack`'s geometry or from mpmath; `tests/test_upper_bound_intervals.py` enforces this. It rebuilds each upstream file from the facts and requires the size and SHA-256 that the acquisition took from the pinned clone. That is the one link between the facts and the upstream bytes this packet may not retain.

**What it finds.**

- **The verified value** equals the exact route's at every count. The exact certificate's side lies within `3.2e-37` of the enclosure of the pose's extent.
- **The printed side fits the printed pose at 20 counts.** At the other 29, the pose's own extent exceeds the printed side by `7.8e-17` to `2.13e-15`: one unit of the fifteenth decimal at 26, and 2, 3 and 2 units at `n = 206, 259` and `305`.

  These are exactly the counts where the exact certificate rounds up. The decimal one unit below each verified value is refuted too, so the gap belongs to the source's pose in any arithmetic, not to rationalisation.
- **As placed in the source's own frame,** only the poses at `n = 102` and `239` lie inside `[0, s]²` for the printed `s`. The other 47 cross a wall by up to `1.87e-15`, so each bound is the translated pose's, as in the exact route.

Three controls on `n = 68` are refused:

- a side `1e-15` below the extent;
- square 31 moved right by `1e-6`, which produces the two overlaps the exact route also finds;
- the angles read as degrees, which produces 53 overlaps.

The receipts are [`receipts/interval-certification.json`](receipts/interval-certification.json) and [`receipts/interval-negative-controls.json`](receipts/interval-negative-controls.json). The replay, which takes about six seconds, runs from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_intervals \
  check --source franciscouzo-square-packing
```

## The 49 Counts

Generated by
`uv run --frozen --all-extras --group dev python -m devtools.upper_bound_packets table --source franciscouzo-square-packing`.
“Recorded before” is the side the case record carried before this intake, from the
retained catalogue or, at five counts, the UnitSquare release.

| n | Side printed | Current since (UTC) | First packing (authored, UTC) | Certified side | Verified here | Recorded before (source) | Live, 2026-09-29 | Casson, 2026-09-23 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 68 | `8.798795237222592` | 2026-09-26 03:27 | the same | `8.79879523722259196327…` | `8.798795237222592` | `8.803383074716108386903836683375989697670063329` (UnitSquare) | `8.7987961402601` | — |
| 102 | `10.607174680178947` | 2026-09-26 22:21 | `10.607902017731913`, 2026-09-23 01:35 | `10.60717468017894594244…` | `10.607174680178947` | `10.61138823373863` (Kingbird) | `10.61138794077522` | — |
| 103 | `10.703516755580015` | 2026-09-26 22:21 | `10.703583456926136`, 2026-09-23 01:35 | `10.70351675558001515097…` | `10.703516755580016` (+1 unit) | `10.703790283762427` (UnitSquare) | `10.70378195534367` | `10.70377984436967189` |
| 105 | `10.806077865540567` | 2026-09-26 22:21 | `10.807588532111675`, 2026-09-26 03:27 | `10.80607786554056745338…` | `10.806077865540568` (+1 unit) | `10.807847913867976` (UnitSquare) | `10.80761933330707` | `10.80758853319602153` |
| 106 | `10.822908044141968` | 2026-09-27 21:46 | `10.822965780538063`, 2026-09-26 22:21 | `10.82290804414196834660…` | `10.822908044141969` (+1 unit) | `10.82297973416944` (Kingbird) | `10.82297973416944` | `10.82293693182615435` |
| 110 | `10.996783396634358` | 2026-09-26 22:21 | the same | `10.99678339663435808932…` | `10.996783396634359` (+1 unit) | `10.996797773597706` (UnitSquare) | `10.99679327401957` | — |
| 123 | `11.601384658385687` | 2026-09-26 03:27 | `11.601386416516311`, 2026-09-25 07:17 | `11.60138465838568691956…` | `11.601384658385687` | `11.60139979378801` (Kingbird) | `11.60139979378801` | `11.60138465962087828` |
| 130 | `11.911187706548755` | 2026-09-26 03:27 | the same | `11.91118770654875555923…` | `11.911187706548756` (+1 unit) | `11.91119052015898` (Kingbird) | `11.91119052015898` | — |
| 131 | `11.954916830219048` | 2026-09-27 21:46 | `11.956521791347278`, 2026-09-26 22:21 | `11.95491683021904856625…` | `11.954916830219049` (+1 unit) | `11.956543108124773261501115489978287643498579738` (UnitSquare) | `11.95652543280926` | `11.95652190193193043` |
| 132 | `11.991327887694469` | 2026-09-26 22:21 | the same | `11.99132788769446886547…` | `11.991327887694469` | `11.99143643966336` (Kingbird) | `11.99137344423646` | `11.99134529315214159` |
| 152 | `12.830718800982252` | 2026-09-26 03:27 | `12.830764338143943`, 2026-09-23 06:26 | `12.83071880098225217592…` | `12.830718800982253` (+1 unit) | `12.83100282216725` (Kingbird) | `12.83095954472600` | `12.83071880600230408` |
| 154 | `12.931663721169976` | 2026-09-26 22:21 | `12.931663789831580`, 2026-09-26 03:27 | `12.93166372116997597927…` | `12.931663721169976` | `12.93171183926903` (Kingbird) | `12.93166712962655` | `12.93166403111078111` |
| 155 | `12.955619592137850` | 2026-09-26 22:21 | the same | `12.95561959213785027220…` | `12.955619592137851` (+1 unit) | `12.95851388606690` (Kingbird) | `12.95844711161529` | `12.95820609164224457` |
| 156 | `12.982082698520427` | 2026-09-26 22:21 | the same | `12.98208269852042740000…` | `12.982082698520428` (+1 unit) | `12.98219172354800` (Kingbird) | `12.98208376048414` | `12.98208269973811824` |
| 172 | `13.618988956935731` | 2026-09-26 22:21 | the same | `13.61898895693573066840…` | `13.618988956935731` | `13.61898898660160` (Kingbird) | `13.61898898660160` | — |
| 177 | `13.822979734183507` | 2026-09-27 21:46 | the same | `13.82297973418350755447…` | `13.822979734183508` (+1 unit) | `13.82302875075647` (Kingbird) | `13.82302875075647` | — |
| 180 | `13.927888140501693` | 2026-09-27 21:46 | `13.932235154395972`, 2026-09-23 07:16 | `13.92788814050169335855…` | `13.927888140501694` (+1 unit) | `13.93513929847193` (Kingbird) | `13.93508705291129` | `13.93500418116475004` |
| 181 | `13.953748821957927` | 2026-09-26 22:21 | `13.954906490904566`, 2026-09-25 07:17 | `13.95374882195792743852…` | `13.953748821957928` (+1 unit) | `13.95698416446504` (Kingbird) | `13.95690672341755` | `13.95679529257278872` |
| 182 | `13.974090713124822` | 2026-09-26 22:21 | the same | `13.97409071312482180038…` | `13.974090713124822` | `13.97442960739443` (Kingbird) | `13.97419105332569` | `13.97409071444282525` |
| 199 | `14.618988956907218` | 2026-09-26 22:21 | the same | `14.61898895690721825923…` | `14.618988956907219` (+1 unit) | `14.61898898660160` (Kingbird) | `14.61898898660160` | — |
| 206 | `14.860158663395859` | 2026-09-26 03:27 | `14.860232206380317`, 2026-09-23 16:25 | `14.86015866339586012403…` | `14.860158663395861` (+2 units) | `14.87253189075152` (Kingbird) | `14.87221902560728` | — |
| 207 | `14.893954634242480` | 2026-09-26 22:21 | `14.893954634353431`, 2026-09-26 03:27 | `14.89395463424247851360…` | `14.893954634242480` | `14.89397859563780` (Kingbird) | `14.89395494255333` | `14.89395465342147418` |
| 208 | `14.937018796984567` | 2026-09-26 22:21 | `14.937471987089294`, 2026-09-24 10:28 | `14.93701879698456740000…` | `14.937018796984568` (+1 unit) | `14.93783044811097` (Kingbird) | `14.93776656277905` | `14.93761283595916289` |
| 209 | `14.955041639430016` | 2026-09-26 03:27 | `14.955093967300398`, 2026-09-24 10:28 | `14.95504163943001612066…` | `14.955041639430017` (+1 unit) | `14.95868244078260` (Kingbird) | `14.95861500087481` | `14.95856148981292932` |
| 210 | `14.973001116591412` | 2026-09-26 22:21 | `14.973488815181152`, 2026-09-24 10:28 | `14.97300111659141217625…` | `14.973001116591413` (+1 unit) | `14.97421396826961` (Kingbird) | `14.97413341886404` | `14.97381035691250695` |
| 228 | `15.604638007678682` | 2026-09-27 21:46 | `15.608976525083040`, 2026-09-24 10:28 | `15.60463800767868282086…` | `15.604638007678683` (+1 unit) | `15.60902282132495` (Kingbird) | `15.60902282132495` | `15.60895620815939289` |
| 236 | `15.872219025616040` | 2026-09-26 03:27 | `15.872415529525043`, 2026-09-24 10:28 | `15.87221902561604032420…` | `15.872219025616041` (+1 unit) | `15.87607676541001` (Kingbird) | `15.87607539315201` | `15.87606262597991957` |
| 237 | `15.911191683008479` | 2026-09-26 22:21 | `15.911196348876377`, 2026-09-24 10:28 | `15.91119168300847876294…` | `15.911191683008479` | `15.91421356237309` (Kingbird) | `15.91421356237309` | `15.91292783720833270` |
| 238 | `15.931725503598480` | 2026-09-26 03:27 | `15.936853396899918`, 2026-09-24 10:28 | `15.93172550359848053224…` | `15.931725503598481` (+1 unit) | `15.93984676308969` (Kingbird) | `15.93965520031394` | `15.93958571370620980` |
| 239 | `15.953819333484685` | 2026-09-26 22:21 | `15.954681985629890`, 2026-09-24 10:28 | `15.95381933348468453351…` | `15.953819333484685` | `15.95643304058435` (Kingbird) | `15.95635358406308` | `15.95623903092502971` |
| 240 | `15.969685337536875` | 2026-09-26 03:27 | `15.974226402938887`, 2026-09-24 10:28 | `15.96968533753687476154…` | `15.969685337536875` | `15.97559404379946` (Kingbird) | `15.97556282833087` | `15.97536577224557242` |
| 241 | `15.988132439537539` | 2026-09-26 03:27 | `15.990091363348586`, 2026-09-24 10:28 | `15.98813243953753907763…` | `15.988132439537540` (+1 unit) | `15.99091684780193` (Kingbird) | `15.99080517810520` | `15.99043971050729418` |
| 259 | `16.602568490497649` | 2026-09-26 22:21 | the same | `16.60256849049765113427…` | `16.602568490497652` (+3 units) | `16.60257141234448` (Kingbird) | `16.60257141234448` | `16.60256850594295841` |
| 263 | `16.742280159187313` | 2026-09-27 21:46 | `16.742448478819039`, 2026-09-24 10:28 | `16.74228015918731342672…` | `16.742280159187314` (+1 unit) | `16.74264068711928` (Kingbird) | `16.74264068711928` | — |
| 268 | `16.878814821018413` | 2026-09-26 22:21 | `16.879116936182307`, 2026-09-24 10:28 | `16.87881482101841138834…` | `16.878814821018413` | `16.87933209237563` (Kingbird) | `16.87931143465371` | `16.87895510935973675` |
| 269 | `16.905967058598858` | 2026-09-26 03:27 | the same | `16.90596705859885841201…` | `16.905967058598859` (+1 unit) | `16.90596764828402` (Kingbird) | `16.90596764828402` | `16.90596713867399714` |
| 270 | `16.937810329390629` | 2026-09-27 21:46 | `16.940571203936592`, 2026-09-26 03:27 | `16.93781032939062854559…` | `16.937810329390629` | `16.94073593015457` (Kingbird) | `16.94062059800744` | `16.94057158197226087` |
| 271 | `16.950820792633813` | 2026-09-26 22:21 | `16.951280889236397`, 2026-09-24 10:28 | `16.95082079263381241106…` | `16.950820792633813` | `16.95509447506437` (Kingbird) | `16.95499909412532` | `16.95479445810086716` |
| 272 | `16.968279785326896` | 2026-09-27 21:46 | `16.969484711401012`, 2026-09-24 10:28 | `16.96827978532689615220…` | `16.968279785326897` (+1 unit) | `16.96980702828259` (Kingbird) | `16.96971602419903` | `16.96944950195848989` |
| 273 | `16.983925962660670` | 2026-09-26 03:27 | `16.986261983467720`, 2026-09-25 07:17 | `16.98392596266066892535…` | `16.983925962660670` | `16.98832058897683` (Kingbird) | `16.98820725030513` | `16.98811467146214582` |
| 292 | `17.597249391199519` | 2026-09-27 21:46 | `17.601260370442159`, 2026-09-26 22:21 | `17.59724939119951890908…` | `17.597249391199519` | `17.60257141234448` (Kingbird) | `17.60257141234448` | `17.60256849240573729` |
| 297 | `17.740417287548325` | 2026-09-26 03:27 | `17.740561448945158`, 2026-09-24 10:28 | `17.74041728754832466309…` | `17.740417287548325` | `17.74116992948972` (Kingbird) | `17.74106074604732` | `17.74092885618564353` |
| 301 | `17.846667192848074` | 2026-09-26 03:27 | `17.846667194079600`, 2026-09-24 10:28 | `17.84666719284807455949…` | `17.846667192848075` (+1 unit) | `17.86899185179999` (Kingbird) | `17.86889155557430` | `17.86867840793058804` |
| 302 | `17.885993892536710` | 2026-09-26 22:21 | `17.886045193506881`, 2026-09-25 07:17 | `17.88599389253671024996…` | `17.885993892536711` (+1 unit) | `17.88674602860566` (Kingbird) | `17.88674602860566` | — |
| 303 | `17.924349265547932` | 2026-09-27 21:46 | `17.928562541013548`, 2026-09-24 10:28 | `17.92434926554793150698…` | `17.924349265547932` | `17.93127894394689` (Kingbird) | `17.93125509556197` | `17.93105636462953001` |
| 304 | `17.934650018395903` | 2026-09-26 22:21 | `17.936633693223122`, 2026-09-24 10:28 | `17.93465001839590355661…` | `17.934650018395904` (+1 unit) | `17.94917201919110` (Kingbird) | `17.94910783564662` | `17.94880191214547338` |
| 305 | `17.952959459023539` | 2026-09-27 21:46 | `17.953672188874847`, 2026-09-24 10:28 | `17.95295945902354086517…` | `17.952959459023541` (+2 units) | `17.96075558628675` (Kingbird) | `17.96066201401205` | `17.96053668235995815` |
| 306 | `17.963449907261179` | 2026-09-26 22:21 | `17.963835795982291`, 2026-09-25 07:17 | `17.96344990726117894500…` | `17.963449907261179` | `17.96926975248972` (Kingbird) | `17.96913960675661` | `17.96846609160515484` |
| 307 | `17.981030548643712` | 2026-09-27 21:46 | `17.981999068165020`, 2026-09-24 10:28 | `17.98103054864371120149…` | `17.981030548643712` | `17.98281564631754` (Kingbird) | `17.98272201579610` | `17.98205200143469895` |

## Parallel Results

Griffin Casson published 39 packings at counts Couzo also reports, in
[`../casson-square-packing-2026-09-23/`](../casson-square-packing-2026-09-23/README.md).
Couzo’s side is smaller at all 39. That packet tabulates both sources’ dates and values
at each, and each case record states them; nothing here infers that either packing
derives from the other.

## Not Done Here

- The interval route above is the method-distinct replay T-056’s `next_rung` named. It takes the result to `C4` once its review is recorded and the register cites it.
- The three trailing counts need a pose refined beyond the source’s binary64 digits, or
  higher-precision coordinates from the source, before the printed sides certify.
- The retained Kingbird catalogue was captured again on 2026-09-30. The page is the same
  one read on 29 September. It prints a different side at 41 counts in range, 36 of
  them among these 49, where every Couzo side stays below it, and five others. n = 126
  and 179 moved to their new sides. n = 69, 83 and 87 wait on intake. The earlier
  sides this packet compares with are read from the 2026-08-22 capture, which is kept
  beside the new one.

## Compressed Files

Two records this packet wrote run past 1,000 lines, so they are stored as deterministic
gzip made by `gzip -9n`, with no file name or timestamp in the header, following the
[R052 packet](../n17-guzhou-r052-2026-09-25/README.md).
The table gives the Git blob and SHA-256 of the decompressed bytes. Readers take the
plain path and decompress through `devtools.retained_data.read_retained_bytes`;
`gunzip -k` restores the plain files for a manual read.

| Stored | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `acquisition/sources.json.gz` | receipt | `ce3c27311e608eb915aba43e28bbe8bf990ffdec` | `7edda23724cfd6eab92c36a7697d99b26c34dcdde7cf0e0ccb28afa40164328f` |
| `receipts/certification.json.gz` | receipt | `f535559251db4083eb38ae040bcc1ba4df3bc6e8` | `5d15b341ec41e40dc8cfcc01d04bb5a7dd8269244000855bea2d0f2261391678` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
