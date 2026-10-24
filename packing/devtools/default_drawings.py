#!/usr/bin/env python3
"""Each count's default picture: its regularized view where the view improves on the
house drawing, else the house drawing, recorded and held to the data; and every count's
regularization state, gated.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.default_drawings`:

    --update [--workers K]
    --check [--workers K]
    --check-state [--base-ref REF]
    --retain-runs
    --compare EARLIER

The owner decided on 13 October 2026 that the regularized drawing is the default picture,
with the house drawing kept as "as published", and that a regularization should be a
strict improvement (`docs/project/policies/regularization-policy.md`, section 12). For
every count the layer's index (`atlas/known-best/regularized/index.json`) draws, the
default picture is the view when all three hold:

1. **Exact.** Both maintained exact routes accept it, as its entry records.
2. **Side.** Its exact side is at most `U`, the case record's verified upper bound as
   `regularize_evand.verified_bound` holds it exactly, or the count is one of
   `ABOVE_U`, the views the policy's section 9, question 13 names above it.
3. **Improvement.** It improves on the house drawing under the policy's improvement rule
   (section 11), which `devtools.improvement_rule` reads from the policy and decides. Both
   drawings are measured as `devtools.regularize_select.today` measures a tree's drawing
   -- the house renderer's colouring by `census_drawing_regularity.regularity`, the house
   and stage totals by `regularize_evand.contact_partners` -- the two sides are compared
   exactly where the house witness is exact, and exactness is the view's gain where the
   house witness is only numerically checked.

Every other count is drawn from its house witness, including a view that ties its house
drawing on every goal: there the picture is the same, and the house is the record's.

`--update` writes `atlas/known-best/default-drawings.json`: one entry a drawn view, with
its default, the reason, both drawings' measures and the goals the view is better and
worse on. `--check` measures every view again and fails when the record is not what the
data gives, when a regularized default breaks the rule, or when the policy's goals or
their directions differ from the ones the code judges (`improvement_rule.problems`). It
lists, failing nothing, each count that keeps the house picture and why: "no gain",
"above U, not in the exceptions", a goal it is worse on, or an exact route's refusal.
It costs about 35 cpu-seconds: the views and their house drawings (about 20 for the 90
views of 13 October 2026) and the other 232 house drawings (14 on a loaded host,
15 October 2026), a few seconds of wall at four workers.

**The regularization state.** The owner, 15 October 2026: "The records should make it
evident which things are regularized, and if not, we should fix the record-keeping
process as well." n = 176 drew its raw house on the site for a day while the layer's
index said `regularized`, because adopting a new house lapsed the grid-slack view
`regularize_axis_components --update-atlas` had kept, and no record said so (think-gvke).
So the record's `states` gives every count n = 1..324 what is drawn, the drawn picture's
measures, the witness it was decided on (its id, its source's key, path and revision, and
its side), the runs that decided that witness, and one state:

- `regularized`: a view of Evan Daniel's regularizer or the grid-slack generator is drawn
  (`STRONG_GENERATORS`);
- `regular-as-published`: the house drawing has no uneven and no near-axis square, no
  strong view of the count has lapsed, and `PENDING_ALLOWED` does not hold it for the
  runs its bead owes;
- `decided-no-better`: the strong generators ran on this very witness and drew nothing
  the improvement rule takes: the layer holds a strong generator's view of it and does
  not draw it, or `SETTLED` says so, by the witness's source and side;
- `regularization-owed`: the strong generators ran on this very witness and none drew a
  view the improvement rule could judge, for want of a capability rather than by a
  judgement, so the drawing is not regularized and its regularization is owed to the
  open bead `owed` names (`SETTLED`, by the witness's source and side). The exact
  algebraic houses are the case (review A4 of #756): grid-slack has no exact frame on a
  number-field witness, and Evan Daniel's regularizer solves each to a rational side
  above the algebraic `U`, which is not drawn, so the exact house is drawn until
  think-mbdw's regularizer draws one;
- `exempt`: the count is set aside with a reason and the bead that owns it (`SETTLED`);
- `pending`: none of these, as at a count whose strong view lapsed with its witness
  (the index's `lapsed`, which `--update-atlas` writes) or that `PENDING_ALLOWED` names,
  even where the new house reads regular, or that only the axis tool's view, the
  reference and fallback, has drawn.

`--check-state` is the gate, reading the record and the index, measuring nothing. The
pending counts must be exactly `PENDING_ALLOWED`: it fails on a pending count the list
does not name and on a named count that is no longer pending, so a count leaves the list
as soon as it is decided and joins it only by a reviewed change that names its bead. A
new house that reads regular does not take a count off: the list's first entries are the
record of strong views that lapsed before the index kept a `lapsed` block, so a count
leaves when the runs its bead owes decide it, or by a reviewed change that drops the
entry (review B1 of #641). So the list is an input to the state as well as a measure of
it, and the gate cannot judge two changes to it: dropping an entry whose count then reads
regular as published, which drops the runs its bead owes, and adding a count whose house
reads regular, which holds it pending. Both pass it, so both are the reviewer's, on the
bead's runs or `--compare`'s table (review C2 of #641; think-k6rj would hold the lapses
in code). It fails, too, on a `SETTLED` entry made on another witness than the one the
record names, and on one for a count that no longer needs it: one now regularized or
regular as published, or one whose strong view the layer holds, which decides it
unaided. Every run a `SETTLED` entry names must be held, under the generator it names,
by a record the retained evidence keeps (`EVIDENCE`, `run_records`): a run's block
(`run.json`) or a driver run's receipt. A block in the layer's index alone is not
enough, since the index drops a run's block once no entry draws from it; `--retain-runs`
copies the block into the evidence (`SETTLED_RUNS`) while the index still has it. Where
the record lists the counts the run covered, a receipt's counts or the reports beside a
block, the settled count must be one of them. A copy there that no `SETTLED` entry
names fails too, since the directory holds the blocks settlements rest on (review G2 of
#644). Each bead the list, an exemption, or a decided or regularization-owed count's
`owed` names must be open, which `devtools.check_bead_tree` holds through `deferrals`, and
a regularization-owed entry must name one. Since the house rule, each entry is
a corrected witness's (`CORRECTED`), which names the witness it replaced; with
`--base-ref REF` the gate reads the record of the commit the change is built on, the merge
base of `REF` and `HEAD`, and holds each entry to it (`deferral_problems`), so a house moved
by any import, a Kingbird catalogue intake or a re-solve as much as an adoption, cannot be
deferred as a correction (review C3 of #660). The records tier passes `origin/main`, or the
first parent on `main` itself. A record older than a
witness is `--check`'s to catch, by deciding every count again. A witness is identified by what
it says of itself -- its source's key, path and revision, and its side -- never by a
digest of its bytes (OR-16); its id is the count's (`W-known-best-nNNN`) and names no
house, so the gate's comparison of it only holds each row to its count.

`--compare EARLIER` reads two records, measuring nothing, and lists each count whose
state, drawn picture or witness differs, with both pictures' uneven and near-axis squares
and full shared sides: the table an adoption gives its pull request for the counts it
re-houses, from its base branch's record (review A1 of #641). It names the goals at each
count whose strong view gives way to a drawing worse than it on a goal of the improvement
rule, whatever drew it: the axis tool's view, as at #657's seven, or a house drawing, as
at n = 176 (review D1 of #641). Where such a count still reads pending, it marks the
obligation every re-housed count carries, that its runs are owed in this pull request:
the owner's rule is to adopt the smallest packing and then regularize it, so a re-housed
count's runs are never deferred (review E1 of #641, and the import runbook's "The House
Rule"). A count its runs have since regularized or decided is listed with the goals and
not marked (review E2).


The site's drawings (`render_frontier_page`), the atlas tiles (`overview_sections`) and
the posters (`build_known_best_atlas`) read the record through `regularized_defaults`,
which refuses a record whose counts, views or generators are not the index's. Reading
it measures nothing: the measuring code is imported only to measure, so its readers stay
light.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from devtools import improvement_rule
from devtools.improvement_rule import MEASURES
from devtools.regularize_axis_components import ABOVE_U, ALGORITHM, EVAND_GENERATOR, LAPSED
from sqpack import retained_json
from sqpack.workers import worker_count
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
INDEX = ROOT / "atlas/known-best/regularized/index.json"
#: The retained evidence of regularization runs, one directory per batch
#: (`<bead>-<date>/<run directory>/`): a grid-slack run's block (`run.json`) and a driver
#: run's `receipt.json`, beside its reports (`n-<count>/report.json.gz`).
EVIDENCE = ROOT / "cases/regularized_drawings"
EVIDENCE_PATH = "packing/cases/regularized_drawings/"
#: The batch of the layer index's blocks that `SETTLED` rests on, one `<run id>/run.json`
#: for each run a settlement names that no other retained evidence holds, copied from the
#: index by `--retain-runs` while the index still holds it. The index keeps a run's block
#: only while an entry draws from it (`regularize_axis_components.carried_index`), and a
#: settlement rests on its runs for as long as it stands (review F1 of #644). A copy is
#: deleted with the last settlement that names its run, and `--check-state` fails on one
#: that outlives it (`orphaned_copies`, review G2 of #644), as the layer's check fails on
#: an index block that draws no entry.
SETTLED_RUNS = "settled-runs"
RECORD = ROOT / "atlas/known-best/default-drawings.json"
RECORD_PATH = "packing/atlas/known-best/default-drawings.json"
CONTRACT = "packing.squares:DefaultDrawings/v2"
SCHEMA = "default-drawings.schema.yaml"
GENERATOR = "python -m devtools.default_drawings"
REGULARIZED = "regularized"
HOUSE = "house"
VIEW = "view"
#: How a refused count's reason reads, beside the improvement rule's own words.
ROUTE_REFUSED = "an exact route refused it"
UNKNOWN_U = "U is unknown"
ABOVE_BOUND = "above U, not in the exceptions"

#: The regularization states a count's drawing is in (the module's docstring).
REGULARIZED_STATE = "regularized"
REGULAR_AS_PUBLISHED = "regular-as-published"
DECIDED = "decided-no-better"
#: Not regularized, with the runs done and no view the improvement rule could judge; its
#: regularization is owed to the bead its `SETTLED` entry's `owed` names (review A4 of
#: #756). Counted apart from `DECIDED`, since nothing judged a view no better.
OWED = "regularization-owed"
EXEMPT = "exempt"
PENDING = "pending"
STATES = (REGULARIZED_STATE, REGULAR_AS_PUBLISHED, DECIDED, OWED, EXEMPT, PENDING)
#: The generators whose drawn view makes a count `regularized`: Evan Daniel's regularizer
#: and the grid-slack port of his placement. The axis tool is the reference and fallback
#: (policy section 4); a drawing it alone made waits for these to decide its witness.
STRONG_GENERATORS = frozenset(
    {"evand-regularize", "regularize_grid_slack/0", "regularize_grid_slack/1"}
)
#: A bead id, which every `PENDING_ALLOWED` entry, exemption and `owed` names.
BEAD = re.compile(r"\bthink-[0-9a-z]{4}\b")


class Settled(NamedTuple):
    """A count the strong generators decided, or that is set aside, on one witness: its
    state (`DECIDED`, `OWED` or `EXEMPT`); that witness as it identifies itself, exactly as it
    writes them -- its source's key, path and revision (`None` where the source pins
    none) and its side; the runs that decided it as (generator, run id); what they
    found; where the record says so; and, where a decision still owes runs or a recorded
    outcome, the open bead that owns them and what it owes (`owed`)."""

    state: str
    source: str
    path: str
    revision: str | None
    side: str
    runs: tuple[tuple[str, str], ...]
    outcome: str
    evidence: str
    owed: str | None = None


#: Both generators ran again on 16 October 2026 at the ten counts decided on 15 October
#: whose decision still owed runs or a per-count outcome (think-0ut1), each on the witness
#: the record names: Evan Daniel's regularizer, and grid-slack at 0.5, 1 and 5 degrees. The
#: #518 runs (`evand-regularize-refreshed-adopt518-v2`, `grid-slack-on518`) and the runs of
#: 12 and 13 October had decided them first, but their receipts keep only aggregates; the
#: atlas README's think-0ut1 paragraph of 16 October gives each count's outcome on these,
#: and `cases/regularized_drawings/think-0ut1-2026-10-16/` keeps their receipts, per-count
#: reports and the selection's report (review A2 of #653).
_LEFTOVERS = (
    ("evand-regularize", "evand-regularize-leftovers-1016"),
    ("regularize_grid_slack/1", "grid-slack-leftovers-deg05-1016"),
    ("regularize_grid_slack/1", "grid-slack-leftovers-deg1-1016"),
    ("regularize_grid_slack/1", "grid-slack-leftovers-deg5-1016"),
)
_README_LEFTOVERS = (
    "packing/atlas/known-best/README.md, the think-0ut1 paragraph of 16 October 2026, and "
    "the runs' receipts, reports and selection in "
    "packing/cases/regularized_drawings/think-0ut1-2026-10-16/"
)
_T146 = (
    "the house is Evan Daniel's own regularized list (T-146): his regularizer and "
    "grid-slack at 0.5, 1 and 5 degrees each draw no change, and the axis tool's view does "
    "not improve on it"
)
_REFUSED_DECIMAL = (
    "a decimal Kingbird witness: the axis tool refuses it (its 36-digit rational pose "
    "overlaps at dilation 1), and no strong generator's outcome on it is recorded"
)
_KINGBIRD = "Kingbird derived numerical facts"
_KINGBIRD_PATH = "resources/web/known-best-packings/sources.json"
_DANIEL = "[Daniel regularized lists 2026-10-10]"
_DANIEL_REVISION = "ea1a2f23678a13bd1d252f9f4c95ca5dd2ffd2b7"


def _ostashev(n: int) -> str:
    """The path Ostashev's compositions of 12 October 2026 keep count `n`'s record at."""
    return f"resources/web/dostashev-compositions-2026-10-12/source/records/n{n:04d}.sqcert"


def _daniel(n: int) -> str:
    """The path Evan Daniel's regularized list of 10 October 2026 keeps count `n` at."""
    return (
        "resources/web/evand-regularized-2026-10-10/source/search/regularize/lists/certs/"
        f"n-{n:03d}.cert.gz"
    )


#: Both generators ran on the fifteen witnesses the adoption of 16 October 2026 moved
#: (think-z7wn): Evan Daniel's regularizer and grid-slack at 0.5, 1 and 5 degrees, the
#: counts 129 to 211 selected that day; their receipts and reports are in
#: packing/cases/regularized_drawings/think-z7wn-2026-10-16/.
_RUNZ7WN = (
    ("evand-regularize", "evand-regularize-z7wn-a-1016"),
    ("regularize_grid_slack/1", "grid-slack-z7wn-a-deg05-1016"),
    ("regularize_grid_slack/1", "grid-slack-z7wn-a-deg1-1016"),
    ("regularize_grid_slack/1", "grid-slack-z7wn-a-deg5-1016"),
)
_README_Z7WN = (
    "packing/cases/regularized_drawings/think-z7wn-2026-10-16/selection-z7wn-a.md, the "
    "selection of 16 October 2026"
)
#: The same generators on the re-housed counts 232 to 304, whose selection did not finish
#: by that pass's stop time; selected the same day (think-r3cl), they draw grid-slack's
#: views at 232, 264, 271 and 302, and decide 237, 303 and 304 no better. The selection's
#: report is beside the runs' receipts and reports.
_RUNZ7WN_B = (
    ("evand-regularize", "evand-regularize-z7wn-b-1016"),
    ("regularize_grid_slack/1", "grid-slack-z7wn-b-deg05-1016"),
    ("regularize_grid_slack/1", "grid-slack-z7wn-b-deg1-1016"),
    ("regularize_grid_slack/1", "grid-slack-z7wn-b-deg5-1016"),
)
_README_R3CL = (
    "packing/cases/regularized_drawings/think-z7wn-2026-10-16/selection-r3cl.md, the "
    "selection of 16 October 2026 (think-r3cl)"
)
#: The exact side of PR 622's certificate at 29 (T-195), as the witness writes it: a
#: 2,399-digit numerator over a 2,398-digit denominator. A witness is identified by what it
#: says of itself, its side included, never by a digest (OR-16).
_PINGYOU_622_SIDE = (
    "24534865107674036688168549876397025785476132874112370099771467927504056975875987"
    "77668145598587502424425421357288609726145808428876745555919765393868948864990206"
    "62286626848533913966633270140339323737234775060697104252262187505267061358915851"
    "79797517343019488443339867249715360890013756666854628979176900944993305442261602"
    "77284218083844005366742091748039518022006666660233451172245387959497299819113861"
    "28340341896665100599050504265681164283786407315438108077478915422848640383699076"
    "43508459843509205620695587608368557533498173488519528447981793482358600152308521"
    "63145956559276701418305250119915193107656287925010688761601527805087597811971792"
    "68992186800118087023909939965361958306702609723503874438188234266623690274961939"
    "45575599138014543670320983369783863929251334778825936608589267984001537304179324"
    "15878924619610880223619348113329454870929533547434625652754461365998474686847046"
    "08577274846756785373467411640198568845679869139347049569273216862095508086041384"
    "57927403334411832210594036476801938126308790969489032002021963023705206483679471"
    "87214968789056661144389943565321419179966749976411146945938503309512793134432345"
    "94489332752841251812776837931042560505314528047253344037905647836681805405579257"
    "44070464684545649032408833632838438910661813484030778674222303675402958374138153"
    "08543924829667973070112669111163074263265363784962579954037987883060749995840080"
    "64456269507685529001800497290208398222379180539136927583744454106959862011788372"
    "54745307861725778970345267181802138568964810374228407899464496680162178116797606"
    "10463125992408924815443704237392503330727294276976623931542451819584620598000836"
    "15350602136442050991498160406550581403871763691753471266519232897389831797360344"
    "53072062298517733929444973959326041866213931560671058617171889088120835739271365"
    "35358856787853147769752657730277662762515348885609987478718547425316041473122468"
    "61515016754027283525809340993977339632387150516279686869114144592751846834247841"
    "63644191544707377182384601048542578683951517983159198963572073487749781532348390"
    "08179306631105379097719789516495945021258170771585856339925841130400359900631907"
    "71676638008750196238260947567192223098009081412463590940694060896119814169874075"
    "70927946930756422932236652442311952880289753229889653917790471125660627044950535"
    "98855543586959655153825911476583276679048841183248477236083548767128421313596442"
    "7186102124863000233796141278872662965770217771690365276248657719966519254396208/"
    "41347411015147748251287955567160422279617987859239061824613584602399184247825674"
    "13226407211403203065887739199609118084844533471798679416900735032687473222139680"
    "76006559094094407823401801537033444312877260793306044400082661776942964688219458"
    "32205999632731242257260717779327387645957779877214823657835103370194812365068788"
    "36287721256689347799807863951388092667648197563925993938390556531505228608954855"
    "29293004672639966571375190573083365201721019066382782566132236506372426288324674"
    "33804926049277865237218259318318863031550635516547101545781692386523673831020787"
    "92000130468658641539801741146889224943442810013209072949461457217339392927864030"
    "59116989288372683988488059416746048774924358905633169025369984204347957808888495"
    "49889513409368609249553227431949773804765028989034108545248182036520277951981446"
    "92092594657450033887027432586825094110442844464606853681664319033486389387445736"
    "21403464889523242930520038312392150147083882481705024302215381042706791295694277"
    "22193918248455604437475474008431950491989305331462855749825302334596428036422858"
    "52596410633979360461440217163898024968451883257550199336829150031495720132797637"
    "31913264598706340450121269932170582476688705368126175248788091174208411171394871"
    "55861188264600298662434129558130752551286136826069371764680379350975554487045698"
    "43358216916775243025949351743902174698612665846213152609786378184952030306093106"
    "80875135425749443779193739755732050366810599520820930553588619142477299518316016"
    "81557959734887161232096934217562946534899419639879634706706759394425997807131721"
    "44359901210230692152439814696253554319377531586894873990381499235730768339867996"
    "86732890744823381024234289923436659737078805465893495441021549009306162829983536"
    "14156505027352742543847229448221211898894817332214805992255410331505217916020972"
    "36911676058943766150551365114305649138572343660857535228979083917905543053139843"
    "75048491274393330770413456336582887012744016602241114055045371164537704080571586"
    "22807992989580395169584310920208363606697557856711363193133466958199740504741139"
    "17337370449084604146353831484738751871298385136659525010746969348827942534339711"
    "92933755977720504524873133357341659688546119774713214582599313041195626495367274"
    "48571787434581111683008052767060968335151345147021365771884720299126238475312830"
    "31692405241550695989903352952233750694266905747073315282264735651376143483435574"
    "343954773982361734961798348911999812513553974602740493739669761924137585813615"
)
#: The strong generators on T-195's witness at 29, run before its adoption on the witness
#: the adoption writes byte for byte (think-30n2); their receipt, reports and run blocks are
#: in the evidence directory `_README_622` names.
_RUN622 = (
    ("evand-regularize", "evand-regularize-adopt-2026-10-16-n29-evand"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-16-n29-grid-0.5"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-16-n29-grid-1"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-16-n29-grid-5"),
)
_README_622 = "packing/cases/regularized_drawings/think-30n2-2026-10-16/README.md"


#: Both generators on the 37 witnesses the adoption of 17 October 2026 moved to T-174
#: (think-3mry): Evan Daniel's regularizer and grid-slack at 0.5, 1 and 5 degrees, on the
#: 35 counts that read pending once the axis tool redrew them, and in runs of their own
#: (`adopt174-c-*`) on 103 and 261, which read regular as published. The selections drew
#: eleven views, 261's among them; these runs decided 25 others no better, and 103 stays
#: regular as published. Their receipts, reports and the selections' reports are in
#: packing/cases/regularized_drawings/think-3mry-2026-10-17/.
_RUN3MRY = (
    ("evand-regularize", "evand-regularize-adopt174-1017"),
    ("regularize_grid_slack/1", "grid-slack-adopt174-deg05-1017"),
    ("regularize_grid_slack/1", "grid-slack-adopt174-deg1-1017"),
    ("regularize_grid_slack/1", "grid-slack-adopt174-deg5-1017"),
)
_README_3MRY = (
    "packing/cases/regularized_drawings/think-3mry-2026-10-17/selection-adopt174.md, the "
    "selection of 17 October 2026 (think-3mry), beside the runs' receipts and reports"
)

#: Both generators on the three witnesses the adoption of 22 October 2026 moved to Evan
#: Daniel's regularized views of 20 October (T-225, think-ql4v): his regularizer and
#: grid-slack at 0.5, 1 and 5 degrees on 204, 229 and 260. The selection drew grid-slack's
#: 0.5-degree view at 229 and decided 204 and 260 (`SETTLED`); 204's entry left when the
#: pass of 23 October 2026 adopted T-229 there and regularized it. Their receipt, run blocks,
#: reports and the selection's report are in
#: packing/cases/regularized_drawings/think-ql4v-2026-10-22/.
_RUNQL4V = (
    ("evand-regularize", "evand-regularize-adopt-2026-10-22-n204-260-evand"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-22-n204-260-grid-deg05"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-22-n204-260-grid-deg1"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-22-n204-260-grid-deg5"),
)
_README_QL4V = (
    "packing/cases/regularized_drawings/think-ql4v-2026-10-22/README.md, the selection of 22 "
    "October 2026 (think-ql4v), beside the runs' receipt, blocks and reports"
)
#: Both generators on the witness the adoption of 23 October 2026 moved to Evan Daniel's
#: certificate of issue 728 (T-230, think-icp1) at 303: his regularizer and grid-slack at
#: 0.5, 1 and 5 degrees. The selection drew nothing and decided 303 (`SETTLED`). Their
#: receipt, run blocks, reports and the selection's report are in
#: packing/cases/regularized_drawings/think-icp1-2026-10-23/.
_RUNICP1 = (
    ("evand-regularize", "evand-regularize-adopt-2026-10-23-n303-evand"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-23-n303-grid-deg05"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-23-n303-grid-deg1"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-23-n303-grid-deg5"),
)
_README_ICP1 = (
    "packing/cases/regularized_drawings/think-icp1-2026-10-23/README.md, the selection of 23 "
    "October 2026 (think-icp1), beside the runs' receipt, blocks and reports"
)
#: Both generators on the algebraic houses the pass of 23 October 2026 adopted once the
#: house writer wrote an algebraic side (think-ot5c): grid-slack at 0.5, 1 and 5 degrees,
#: which has no exact frame on a number-field witness and draws no view, and Evan Daniel's
#: regularizer, whose solves are rational sides above the algebraic `U`, held at row 4:
#: no rational view is `same` or `bound` at an irrational side (result-import.md, "The
#: House Rule"). Its first run timed out at 258, 259 and 302 on a host at a load of about
#: 25, and a second ran them at 2,400 seconds. Each count draws its exact house. At 153,
#: 207, 259 and 302 a strong view of the earlier rational house lapsed just above the new
#: `U`. The owner answered question 13 (think-r8cn) on 23 October 2026: the best record is
#: always the record, and a regularized drawing may change the side only as a strict
#: improvement. So no view above `U` is kept or drawn and `ABOVE_U` gains no entry. Each
#: entry is `OWED`, not `DECIDED`: no view was judged no better, and the exact house drawn
#: is not regularized (review A4 of #756). Its `owed` names think-mbdw for the
#: regularization of the exact house, which needs a regularizer for number-field witnesses
#: and a second exact route to admit its view. `PENDING_ALLOWED` cannot hold them:
#: since the house rule it defers only a corrected witness (`deferral_problems`), and an
#: adoption moved these. The runs' receipts, blocks, reports and the selection's report
#: are in packing/cases/regularized_drawings/think-ot5c-2026-10-23/.
_RUNOT5C = (
    ("evand-regularize", "evand-regularize-adopt-2026-10-23-n70-302-evand"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-23-n70-302-grid-deg05"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-23-n70-302-grid-deg1"),
    ("regularize_grid_slack/1", "grid-slack-adopt-2026-10-23-n70-302-grid-deg5"),
)
_RUNOT5C_B = (
    *_RUNOT5C,
    ("evand-regularize", "evand-regularize-adopt-2026-10-23-n258-302-evand"),
)
_README_OT5C = (
    "packing/cases/regularized_drawings/think-ot5c-2026-10-23/README.md, the selection of 23 "
    "October 2026 (think-ot5c), beside the runs' receipts, blocks and reports"
)
_OWED_MBDW = (
    "think-mbdw: the regularization of the exact house, which needs a regularizer that "
    "draws an exact view of a number-field witness at or below the record's side, and a "
    "second exact route that admits it; until then the exact house is drawn"
)
_DANIEL_639 = "[Daniel exact current records 2026-10-16]"
_DANIEL_639_REVISION = "7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1"
_PINGYOU_574 = "[PingYou PR 574 certificates 2026-10-13]"
_PINGYOU_574_REVISION = "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde"
_NO_FRAME = (
    "grid-slack has no exact frame on the number-field witness and draws no view at 0.5, 1 "
    "and 5 degrees"
)
#: Why a rational view above an algebraic `U` is not drawn: the owner's answer to question
#: 13 (think-r8cn), and row 4 of the policy's obligation 2.
_NOT_DRAWN = (
    "which is not drawn: a regularized drawing changes the side only as a strict "
    "improvement, and no rational view is same or bound at an irrational side"
)


def _held_again(margin: str) -> str:
    """`_held`, where the regularizer's first run timed out and its second solved it."""
    return (
        f"{_NO_FRAME}; Evan Daniel's regularizer timed out at 600 seconds in its first run, "
        f"on a host at a load of about 25, and in its second solves it to a rational side "
        f"{margin} above U, {_NOT_DRAWN}"
    )


def _held(margin: str) -> str:
    """An algebraic house's outcome where Evan Daniel's regularizer solved it to a rational
    side `margin` above `U`, which is not drawn."""
    return (
        f"{_NO_FRAME}, and Evan Daniel's regularizer solves it to a rational side {margin} "
        f"above U, {_NOT_DRAWN}"
    )


_T225 = "[Daniel regularized lists 2026-10-20]"
_T225_CERTS = "resources/web/evand-regularized-2026-10-20/source/search/regularize/lists/certs/"
_T225_REVISION = "0075967bace18a3deabcc0baa64c2fb294fc80a0"

#: The counts whose drawing is not regularized and not regular as published, settled on
#: purpose: each named with the witness it was settled on, so a new witness makes the
#: count `pending` again. Written from the evidence the audit of 15 October 2026 found
#: (think-y1x3); the run receipts keep only aggregates, so `evidence` says where each
#: outcome is written down, and `owed` names what is still to run or record. The ten
#: decided counts owed think-0ut1 runs or per-count outcomes until its runs of 16 October
#: 2026 (`_LEFTOVERS`). Recording each run's per-count outcome on the index, so that a
#: decision needs no entry here, is think-4ov9. The gate fails on an entry whose witness
#: has changed or whose count no longer needs it.
SETTLED: dict[int, Settled] = {
    29: Settled(
        DECIDED,
        "[PingYou PR 622 certificate 2026-10-15]",
        "resources/web/pingyou-pr622-certificate-2026-10-15/facts/n-029.yaml.gz",
        "31155575ce1e6b461f77bfc9f3e201adf101115b",
        _PINGYOU_622_SIDE,
        _RUN622,
        "grid-slack changes no square at 0.5, 1 and 5 degrees and ties the house drawing on "
        "every goal; Evan Daniel's view, 5.93e-20 above the certificate's side, is held at "
        "row 4, and his same-side re-solve refuses the certificate's 2,399-digit literal",
        _README_622,
    ),
    39: Settled(
        EXEMPT,
        _KINGBIRD,
        _KINGBIRD_PATH,
        None,
        "6.8107220830686488516977794443517526346472763123335",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
    55: Settled(
        EXEMPT,
        _KINGBIRD,
        _KINGBIRD_PATH,
        None,
        "7.9457710075039129789580095385274780713965449730227",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
    68: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-068.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "929681207264358423472447734663842353544712296027934571642659724802695262831518"
        "066785358670746872082489432142934671956597915411239497251630337522271085517445"
        "622515762840344032037161663328667527471267466117523970718617413700884497032235"
        "5579194107487018099253642045085283732525025286559935/1056600571100771183749261"
        "187443033325390495084119727074531770304234311920295383017609296645477449604555"
        "608283511875119932868401074842185927030175152572735402624973730937773037226920"
        "838854442380447085914701328645860460427517009221703698952120142237130389011811"
        "364286948629355167571657144",
        _RUN3MRY,
        "Evan Daniel's same-side view and grid-slack's views at 0.5, 1 and 5 degrees "
        "each tie the axis tool's view of this witness on every goal of the "
        "improvement rule, and his solved view is held at row 4 (solved about 1e-19 "
        "above U)",
        _README_3MRY,
    ),
    84: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-084.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "643848336672378144388330971905263096473299811191218206394905407404656989308393"
        "758025217071610231666737538564016203250451453535531735003610521318534480388660"
        "376021020379809831875350191184275109547523803708422931841876965601518064883643"
        "879798749343690306770736088274942389043353555402079/66390252153249964848490970"
        "128851986115452292249127039433602332899858427040521450875992257319377684357754"
        "397985211363615917122487043330833624519279861420299203763062813702520502655643"
        "439486627578101219474036231278819400620924130776903984784590846522947312025217"
        "853673052062616008141844",
        _RUN3MRY,
        "Evan Daniel's same-side view and grid-slack's views at 0.5, 1 and 5 degrees "
        "draw no change, and his solved view is held at row 4 (solved about 1e-19 "
        "above U)",
        _README_3MRY,
    ),
    86: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-086.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "747006558015504798302738133119714840926878053666735648180539553919696972428914"
        "204890714553258186740743424243711594196641336092871509540352947296613988751347"
        "266253888455730749047542501395039192831203221005360874082619558845273944074707"
        "256235410212663877421093461196296785919799607486664769961474087449726370973304"
        "613014836767877849459433196893483264211123745725539455314796752433986682441103"
        "948133069031186656966819662760860201608841171693703387189576564677166307840733"
        "8224233/7606576698916632917882309203756583714151080929171963479010227814904697"
        "486397593532374940965756104462132288557867049630261359061661126954881342824568"
        "316663426582268854749592686115907449381761548780674818474014072464178380227255"
        "887731418103532920241051138467150681463674165533175007503725480393055744527848"
        "081743424069863202988483802349761681688850418660195344283951525797765562694717"
        "687475419343028710152372684282366127268886838745848288664707127405785277651810"
        "42538897450833",
        _RUN3MRY,
        "Evan Daniel's same-side view and grid-slack's views at 0.5, 1 and 5 degrees "
        "draw no change, and his solved view is held at row 4 (solved about 1e-19 "
        "above U)",
        _README_3MRY,
    ),
    102: Settled(
        OWED,
        _DANIEL_639,
        "resources/web/evand-exact-cur-2026-10-16/facts/alg-n-102.yaml.gz",
        _DANIEL_639_REVISION,
        "['67/4', '25/4', '-105/4', '-27/4']",
        _RUNOT5C,
        _held("1.06e-19"),
        _README_OT5C,
        _OWED_MBDW,
    ),
    108: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-108.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "784486179677573581991671750502627647690849586315837067524969581719432573131816"
        "575701996805775810683190356963481048249437688278531515088276722668684203536782"
        "312550970389724710204791776796466633913283058017708370027620419738095784643318"
        "869869830251266633372895467029627071662430818071267/71939390732892786308108684"
        "741508629641699074976010803840294931177844619752318328260334740244990201471845"
        "694327319816922121412586841233786246385477865838612662698183807605944712358552"
        "400692382953629903438860750830990483480097357305500507667288338480599543227312"
        "734648617526189636189266",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    110: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-110.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "173663815675352328522530738839649178226370429052114325009565122468752427566886"
        "040142496939572547493521538871680177886784685660067988558300505781759247494661"
        "791942728494500785058547542251774176011048347398804454467035404350036123234434"
        "848224817204803415547359683034194634769162292208343541134082649175571991442487"
        "394708127760439461079943569185448096251767985047595371779536995527962679995953"
        "826638334532585420844178952672877775942200282290018325642025194505348498748062"
        "456373477493862527761942600162717120167739854981234821624096515931832889769009"
        "164597048494365339623904693568519457109459470222225020128893895482406922552793"
        "7323799708655609575735471205730940600/1579223754907703588249269126053785486371"
        "752362463141869376321253053109519120271730434673878166738824513913598652614238"
        "454765866139956780124134134449691850542455748662727412191191486264540500089910"
        "974195167465803747776488864888942376178820916895746250164107351819791927612932"
        "735820352394699021986494301057736801334046672197781033284895497161993360298449"
        "128214536858594727925824994547374229118602390855917987070430218418640865149535"
        "847850044284281604602441378797057152521204550826379240407311414768190569989314"
        "566854718688690015477903135669294529997582120838968716451199101318897286882839"
        "17771128103651336300108117008007118650473164721287977855213489447690135489",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U), and "
        "grid-slack's views at 0.5, 1 and 5 degrees are refused at row 7: worse than "
        "the axis tool's view on light and uneven squares and both totals of shared "
        "sides",
        _README_3MRY,
    ),
    123: Settled(
        OWED,
        _DANIEL_639,
        "resources/web/evand-exact-cur-2026-10-16/facts/alg-n-123.yaml.gz",
        _DANIEL_639_REVISION,
        "['33/4', '10', '-6', '23/2', '-33/4', '1/2']",
        _RUNOT5C,
        _held("1.16e-19"),
        _README_OT5C,
        _OWED_MBDW,
    ),
    127: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-127.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "135498536094691656518840302064514115294542468016226400014199451957145619817818"
        "540810178220264676019962366284978593757592312767615344487718300447600244313196"
        "410894217701147358186228992617922292138047804585614932138977858328658631503049"
        "767834454372611964435874412134384772911945898712395990568273081346030515083644"
        "680793466355542912350299874514184892678819300042905045000848034914843613019526"
        "150569319197864659154008470196129176297253011415657909588271800757337965097268"
        "244731531/11472350070773135870738664984884771824240519173376928166846447271962"
        "181482698376590799910042055451537469277860534944156990094530050859887280911833"
        "518571890816974225740486914904215376569885447307269234078535071645003843008473"
        "664677728271135218388461117144501113959721371541098765701449634712221142863779"
        "884574231106787879705830596466720112479423463036006094003783613697035648679089"
        "255034048384043441345133675219950369224788645308472728992856849918581294863698"
        "036325476448808712",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    130: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-130.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "250921464426882526303653169444097829020975824604307281852283011150757058972142"
        "559969508496172961666302963431279497075633541250382195347705070483299813279732"
        "120803415845130053665317070347794000297375467816283442942105324756902590703389"
        "762189595274660221120162013731841444785581667218733460781039048372045906093721"
        "641915027738610404907366317458762709749494320115312427695750893237805080173259"
        "921618987357336278548606212241918660577652398872568422877877379895579591535822"
        "3826791/2107789676725298666193661675755847082298554798063725330136427543187126"
        "674954075453066950489002673582475888549692886919732983408156930751180612925892"
        "073217848812306928019525930798318698961001915305820299106403652691400131087029"
        "853506075984904755752346967894631198747712195221280373396628964268330754468916"
        "035604179611823576547135236151090337594307674661313709595700408396816941459410"
        "703443698843111009821340837624580865588367194479454858056853771905732163621753"
        "60455585267880",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    132: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-132.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "330741141472971891752525638916268099190405651568227696856704748111804993903234"
        "544824692742563267471366087272519939719862775272482615515511940205796407879977"
        "623138902744671520621182831612781005756922291501663623607999015437858787584923"
        "741134089237988126556723621312460601401465496067086785787167947007446517513853"
        "727237321313516231967966271862199341844272166972287839215142478543390817619512"
        "619117827183090547306030624141902964527982272653764631651515952706487627761481"
        "68747513/275946909967463874893845848449072515987769045935967960920393567952818"
        "897553710616137428695538913967791341453030878097615394432058980078993877239822"
        "476213401346108751123539753545407955276110529059530588329921217650534199572672"
        "315324596256562541151944620121207001759339148926675382326949517250104509227042"
        "279571998341658352279115211051629099388551808435073135571241582399088460704596"
        "783429597069815913961869057090929886096862856311382647609816048846134375256835"
        "5930089397710507",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    153: Settled(
        OWED,
        _PINGYOU_574,
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/alg-n-153.yaml.gz",
        _PINGYOU_574_REVISION,
        "['2043/164', '155/164', '27/82', '87/82', '-243/164', '355/164', '-19/82']",
        _RUNOT5C,
        _held("1.29e-19"),
        _README_OT5C,
        _OWED_MBDW,
    ),
    176: Settled(
        DECIDED,
        "[Mishapolk KKT refinements 2026-10-14]",
        "resources/web/mishapolk-kkt-refinements-2026-10-14/facts/n-176.yaml.gz",
        "70a033f0ecfa9e643cd5fb5dbac190cb7f4ffb94",
        "13795872318436407263173895330727713371233106699551510374450211701529164297205177"
        "6912348029686675350647263/100000000000000000000000000000000000000000000000000000"
        "00000000000000000000000000000000000000000000000000",
        _RUNZ7WN,
        "grid-slack's views, admitted at row 10 at all three thresholds, draw more uneven "
        "squares than the axis tool's view of this witness (worse on uneven, better on both "
        "totals); Evan Daniel's same-side view is refused (its literal is too large) and his "
        "solved view is held at row 4 (solved above U)",
        _README_Z7WN,
    ),
    179: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-179.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "633623811190746643479884505475771579015670596141459749084386172048189662237909"
        "387768608210996858604245967567884947308023476651605782792368384356665613496796"
        "255789465066717889450211342784010306101275867663851001085653029078076845090437"
        "6205618905474742150835470970130080373399871451707/4563765085878763825287779650"
        "351406931178147045231598627106378914144698040567906497454406515088567583661809"
        "587983789662616086382763052404581936167428866533709354906907039039875673855245"
        "681436318195008323311050101670105215678875972177933710147852286686061339899161"
        "34021565891836642047",
        _RUN3MRY,
        "Evan Daniel's same-side view and grid-slack's views at 0.5, 1 and 5 degrees "
        "draw no change, and his solved view is held at row 4 (solved about 1e-19 "
        "above U)",
        _README_3MRY,
    ),
    180: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-180.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "155025071816638739375920062838973091822976073002980368747210126605852720649780"
        "417647109197446301149543571551755227757385929209582336869098517573907666164058"
        "591390993846669032590361599387262694283676957458118848978158186527057716197716"
        "7375393786132252959632859942696323050956793319412034/1113926449460885485630252"
        "817228660364340154725382597603439982237063155721544698609036724925314374797939"
        "461433885545711541904570251436349681422966777467674634410710614191872023681777"
        "015649365843410343697085341552585661859445060494127788703323993064975543431992"
        "21015096444019032359522413",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    182: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-182.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "237833923949347406319344341313918385648342762542430301654765472403146098264002"
        "225697299110447592672534234872259579846496056669841395644437305106229929948216"
        "478744529314088679114449753545618507820313689859766896950510129312476038619180"
        "441987389419700474268589141152650429566346575714844794676432490829829800848595"
        "531261901843644272962748175982068113270548496420488260312318999094595359117392"
        "938331097759755961704917457466153260549084000783785017509045889320360081009416"
        "779496/17019635039725719200033994032590707268320512800859475098368213904340007"
        "770774821972775712669157491717457634571096631353107150408590579013989521902380"
        "383602817384052405528382295252799642943866310900148457185587559632916505646661"
        "845763889979722770708986111059505537068685689596996974072649006499835073825634"
        "729369470186080314125795115380160824610322474283053008014793811856179250205296"
        "316363761431986577533171776889611878418485809785946237792494137882238966754418"
        "286050484157",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    207: Settled(
        OWED,
        _PINGYOU_574,
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/alg-n-207.yaml.gz",
        _PINGYOU_574_REVISION,
        "['1288/89', '209/178', '-78/89', '335/178', '-12/89']",
        _RUNOT5C,
        _held("1.49e-19"),
        _README_OT5C,
        _OWED_MBDW,
    ),
    208: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-208.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "244337722756614881947904606513320201490581227795561103036344169239122759470663"
        "709072243749437495607797007171810630029252773599638037131220289587214774637276"
        "170745093112169016651031100229836118182824430215092328823015501164347923342823"
        "197134457172229998629024531739549878705274188567029778659391592076034273080109"
        "741132053583559435144392806490300443944843635196092131201204130986465362476425"
        "617877005993032020677262999556238950/16371564570278680484751897861265524087888"
        "488370784709062226348587123820258650942158462067366428318298277786625630152850"
        "003470950258928993064051012823853626225606385988741677340779596770163853076200"
        "671207882324160231142848859870688323163495056542936932146532446038920443793258"
        "796318215074124100102971089938482904688852559307234252742490902114291898386420"
        "412410987283598704613377092247288341299163355582395905801288406437968727",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    209: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-209.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "371631425503885720434685536400475957243021764553498251652441268436843733965091"
        "811718257636557969551571857281735323653226234550389543493188239500235588160281"
        "967509005018047099289179848152690079289283917705906247582656270052153612689325"
        "849097613198456443699192332658697524476361933328333939613081819258513207809401"
        "109590211276754214098153911388606128195686134934083594307620823814826880068362"
        "880836684184910359830122101328544270693925096721371549390278745943748448859035"
        "945911/24864570793128933465141343508302379246129312968503956629644145329043816"
        "714219147352879048448267869086566630755890929539102829705799918153795190652564"
        "872530053067236690704358356563853740672920852310662909032793813002983761060395"
        "909535209506891166278496027720227080792399400581984949467518382332715498075703"
        "639634776049775740958054888473304487100637155338515082484497957619279274318887"
        "264329553422773232265767872549954847406053847733483992092413452674122091791373"
        "846780644819",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    210: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-210.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "213379360444021050689203190496093099957497304050899741677021692160272467323354"
        "170616184614618931795359963510023796673706647682873687211780740008366836118479"
        "797252007672090560557886876196231231242988231790588081216034663166030257015830"
        "205287873409860786631502941784656008418818149396734436328133200240045652039018"
        "694425501985605210521309907100697373686789184174647873858421495041300899968122"
        "898814546914978956565867713168580151442152427084353088818184739484401715454911"
        "834512508824866533650901408617034802462402442978205839712311077796297380443328"
        "212651144103668977245997223772175979740726893794/14250941329833453992139349996"
        "721591135758230191335730890861281929301090539389878777211878713921101915188956"
        "676794703430073537275446352186803549515086096129711156488178667617697449870039"
        "375223575152989214756496714556866877906021772861863607049147070529984091943236"
        "392511555088842599423653140588891975101627546786576135587971254504992689860389"
        "298696805389866072461467784155474584090923147078625681331326849123362151234818"
        "599437245068693481430681457617426232493310648171918210599254030973602818883467"
        "081384249218961053556054119765855366418973183716465936870735950587281063981178"
        "360238698016662359",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    228: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-228.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "819486956222427434065838854556296435515888934151427614630092120369644833117556"
        "039448104315966648179462605733217414292381343616991657052470805939640487660620"
        "426879920064276697278749018283614028631455498143890842621261204280638890820734"
        "712906429323944800731179720647781901202137909117069812583845222036212652665331"
        "179513582599377049658313223899216547026567503163152289472875876258728022078455"
        "094832042010996996761328350609147532400322612448654764542489093484190008881892"
        "90166/525157247685563248366746065785287543925418240602052988075354819092404618"
        "566980135334828175799072844156754253325417094237105752149667670692223375175108"
        "319675827585781705227366233060212608797260303410593242463677254737570034238567"
        "695832506381375190527631078920495575552963285753861575662875420541624554743275"
        "072280539553231888830390973210068583013267994048846579655759147075410546688021"
        "973925174813607763037593035155380705974005312455782512992290822334714088168782"
        "4268888523",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    237: Settled(
        DECIDED,
        "[Couzo n237 2026-10-15]",
        "resources/web/couzo-n237-2026-10-15/source/certificates/n237.cert",
        "58a783368d4b7e70bb800f0009ea9ca03e578739",
        "7951301819129798440089572127137/500000000000000000000000000000",
        _RUNZ7WN_B,
        "every view, admitted at row 10, draws one more light and one more uneven "
        "square than the axis tool's view of this witness (6 / 10 against 5 / 9), "
        "though no near-axis square, no more angle classes and more shared sides: "
        "Evan Daniel's same-side and solved views, and grid-slack's at all three "
        "thresholds",
        _README_R3CL,
    ),
    240: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-240.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "483779079887851453071822038668856961350375295848725851709478355575859169191912"
        "130791877860446114844693376382167345229478318591100613731678417966396101612915"
        "507679560475375556249444274034377950652576304328460691024335312757845809887576"
        "649855038209052677749442036321082727681911578300352262565761442000479729789298"
        "483051210051984871918828380121740015335779339133507724353566807617434364374669"
        "000687185738985352433089007563616028362668780396929684179145098688283802397809"
        "237464729407551166454337025574569596940829335543928436152104388992301857438488"
        "570049564308037707952730572603200375653122984207583430007973218863934187607482"
        "1494678865298876808894448151899978184021/3029358873783877435368188535373167823"
        "759542531181313145201557671779354788201961074116910669266689921741520516911924"
        "818599562159391625687650487763112477249747699889728368019878188200429754234197"
        "994218657688327376318554847276283522549068463275983751274350832807417385793148"
        "708821132380213587237092925205097768581660265542271013269228904254351398058902"
        "927595524065471786385476235858035927372649235041139653583856085224363890416447"
        "802080444133099064223104952677199887239341330748025727443062299690553001006260"
        "150732689946397168208724825250355194958933123745688515878986732916239610965582"
        "266100077350416927390689524378890839268610597279878318975082794602240839068439"
        "64",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack finds no view at 0.5, 1 or 5 degrees (relaxed rows "
        "overlap at this side)",
        _README_3MRY,
    ),
    258: Settled(
        OWED,
        _DANIEL_639,
        "resources/web/evand-exact-cur-2026-10-16/facts/alg-n-258.yaml.gz",
        _DANIEL_639_REVISION,
        "['8681/544', '2003/136', '-26795/544', '-10137/272', '163247/544', '-25131/68', "
        "'87875/544', '-6877/272']",
        _RUNOT5C_B,
        _held_again("1.66e-19"),
        _README_OT5C,
        _OWED_MBDW,
    ),
    259: Settled(
        OWED,
        _DANIEL_639,
        "resources/web/evand-exact-cur-2026-10-16/facts/alg-n-259.yaml.gz",
        _DANIEL_639_REVISION,
        "['53/4', '-10', '-6', '-23/2', '-33/4', '-1/2']",
        _RUNOT5C_B,
        _held_again("1.66e-19"),
        _README_OT5C,
        _OWED_MBDW,
    ),
    260: Settled(
        DECIDED,
        _T225,
        _T225_CERTS + "n-260.cert.gz",
        _T225_REVISION,
        "4161438312629953048686574163329/250000000000000000000000000000",
        _RUNQL4V,
        "the house is Evan Daniel's own display regularization (T-225): his regularizer's "
        "same-side and solved views and grid-slack's at 0.5, 1 and 5 degrees each draw no "
        "change",
        _README_QL4V,
    ),
    263: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-263.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "191358566429320512421095057854855969998357940938632270984672258592509021289344"
        "968511666831431664456722054747573879847422310508347665037614043240410195640259"
        "176571870066619664264257691408377679223326177197170250036108668241403127097889"
        "153493130517553930882970007086387477028239366671788149031538849165541229712295"
        "788178901300871429586172396513563614934464602215157911551615472636200797123810"
        "210585100529825661832874894185456534209564921479596392746669341014754460826509"
        "79590406/114358852556045951449821660803512063862609877137814007835165047866048"
        "243815521804488716132658335967227467450522232351297241958176977939507799052975"
        "729846084010245989983505220109795160678467519763594213717801148110202183051097"
        "426204115692303999522860150047359938125720544897951695711477008591425610043441"
        "880969978575653756889944455620790760987162369811606619677277101050950570128177"
        "454511078802116279708162450496189460505371637355985365131861633363330466077868"
        "4040092050738379",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack finds no view at 0.5, 1 or 5 degrees (relaxed rows "
        "overlap at this side)",
        _README_3MRY,
    ),
    268: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-268.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "233270980632039540411435419500234711630560155576630993915611543452774739703722"
        "952929556646506050679237827213781742529692622682547843177659465028768064414144"
        "931073857091973918513911796469530253808279283824665291827193594194760245545948"
        "876956412126275759753119941151135458159232318443962/13820341244677848083924813"
        "816260807677337124572759119046734684346629144601651358267843383787847827349194"
        "959910412847847999665748703540707032408725232782401407917969030977642092448911"
        "296381546041810733285455019634473955659876261312467110209743680075779870696203"
        "555758879668577135424641",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U), and "
        "grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    269: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-269.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "762455321661214625154064717575663643223209516170114617954836114502409073914917"
        "350306062684974688108175698138394198328039661482509815313961445914973037400188"
        "315008896501350993871128847488533369930209358303422921792499221423993238497834"
        "934040341710705797262200466540592661253334264548983/45111659257824839102395844"
        "510075287639411941931091142308133831539304493554725538730586505928273109944096"
        "508731943061625604172188642108802879488059456112093682097138673317692898853025"
        "765103795703325919365728472905467297061887465330632167402750760142429709049654"
        "398016240842352148167624",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U, no "
        "change), and grid-slack's views at 0.5, 1 and 5 degrees draw no change",
        _README_3MRY,
    ),
    272: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-272.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "632033032744118982344009456733441947852201554208800271553798395796432288990570"
        "954468505378015897401809451197296065381292296760740957069169803406335644187546"
        "745967340630238268921306168038292303051252426152268565113513638589926919865001"
        "329331500422673270395318459307440598524728167375399207649418410413206025151678"
        "366791713485102434321276663299275357873388642146992239248683226666300344372534"
        "433818838255969602808332174683952863895305878732267193999244505164691383450485"
        "654673856491474914527473470741734220848419623950315055341323159764490008185313"
        "503668685219801477854762566/37253827545632569856984407294134180727756188767374"
        "264273854576331409009755965554896159402208851217350738332802015778072345878143"
        "678134867365134070729488130415606021936200424643500800677294196601828844937381"
        "836728782021019477734444162800444327458340685659960956965354517946980342143777"
        "282088833877834882263796888293399445229883153943238396097878304605400582309488"
        "474438073578126462300021832995054715040778634898158951951980241112646280841653"
        "410648105648190718095057130940333879920159107788444333360142185484165429071222"
        "723823611255723669090649000616183698762504367506925303",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U), and "
        "grid-slack's views at 0.5, 1 and 5 degrees are refused at row 7: the stage "
        "total of shared sides falls against the axis tool's view",
        _README_3MRY,
    ),
    273: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-273.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "174543030997781817984168408548026363538284225762969858312924281982408678262222"
        "631415925518087288995370678062691348204972317487783035327625430568663969506372"
        "542472640552167418226765717326241265634207557342100138155332749486668002747347"
        "72589513931159489342183563660935868652540617895453837/102769543026519254765823"
        "230712975121323442090656291080488544925914308403029501768828407407543099944172"
        "777861037397305646415920114981222999023279437696844097424156212171842964754529"
        "501821283800887392286345248064895535690579817427387828786643542945716151599947"
        "0783203722668149292198621809",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U), and "
        "grid-slack's views at 0.5, 1 and 5 degrees are refused at row 7: worse than "
        "the axis tool's view on uneven squares and both totals of shared sides",
        _README_3MRY,
    ),
    290: Settled(
        EXEMPT,
        _KINGBIRD,
        _KINGBIRD_PATH,
        None,
        "17.53553390593273762200422181052425",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
    291: Settled(
        EXEMPT,
        _KINGBIRD,
        _KINGBIRD_PATH,
        None,
        "17.53553390593273762200422181052425",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
    297: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-297.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "101472464323768792245904284543375474230555638453919578463733874774559530240921"
        "796792735523846207099103202422615058339983630007196089896766991483740867721667"
        "472916181572269715834763092162768289696214262722220496581436740329667491992470"
        "385588085302831190869100320592567888502647361261272797960903099925533059078417"
        "429905087434713621596035551277929270182148134551280954705208376703496488535181"
        "163507406261488638141906227450903477512322347617174097593298009022893926125113"
        "158834843390701473172549156227486488485336454113392032916041278678136092861880"
        "714914125104000339150069207041486952229136779363920730721882582452975716844475"
        "544551508425850620449911914183287655383495697476433982807143529755491715467190"
        "957715249168323828398934353363258835081365949059791777270378889679221320876989"
        "1349919882220390497356350587355960673096877261161822776515148405970758147782/5"
        "719846533430548674203078792439336393621731481938234825416678389927869848489027"
        "877708066734232047947137898972962775609360488188416493204427088723993241944454"
        "799676029355918789765977508446988496657465337902752489231712573562300516122045"
        "534866041540641672755317142321730275229664454497186112262952127162776339672486"
        "261780225171883834157956874357967989176612445253960517217212910393328705639027"
        "284783238100329138618575079038839202957768898848137306692783133978181959092724"
        "854554789952501742000569044182361051414453459246839227984250482400578136931797"
        "879673891932961186820374671676841931854018610437219256644150165082229962721906"
        "019098533504551291534383695277344580904241761440617232506027356096622336718904"
        "533869257644312426513742119915109402556450217842041957939001871119160026896464"
        "0211800250714276006224877779479559693213270601792473480819619316765587763",
        _RUN3MRY,
        "Evan Daniel's regularizer yields no view (upstream's checker refused its "
        "certificate), and grid-slack finds no view at 0.5, 1 or 5 degrees (relaxed "
        "rows overlap at this side)",
        _README_3MRY,
    ),
    302: Settled(
        OWED,
        _DANIEL_639,
        "resources/web/evand-exact-cur-2026-10-16/facts/alg-n-302.yaml.gz",
        _DANIEL_639_REVISION,
        "['2863/164', '155/164', '27/82', '87/82', '-243/164', '355/164', '-19/82']",
        _RUNOT5C_B,
        _held_again("1.79e-19"),
        _README_OT5C,
        _OWED_MBDW,
    ),
    303: Settled(
        DECIDED,
        "[Daniel n303 2026-10-22]",
        "resources/web/evand-n303-2026-10-22/source/search/packer/candidates/s303_r303w0.cert",
        "f06521f4bde9e379a91c1ea88053f3e43df8ede5",
        "447744305431858194305431410441/25000000000000000000000000000",
        _RUNICP1,
        "Evan Daniel's regularizer finds the witness not first-order jammed and yields no "
        "view (row 1), and grid-slack's views at 0.5, 1 and 5 degrees, one view at the "
        "witness's side that straightens its 15 near-upright squares, are sent to review at "
        "row 7: better than the axis tool's view on near-axis squares, angle classes and "
        "both totals of shared sides, and worse on light squares (13 to 12)",
        _README_ICP1,
        "think-ykgh: the owner's row-7 review of grid-slack's view at 303; until a review "
        "record admits it, the axis tool's view stays drawn",
    ),
    304: Settled(
        DECIDED,
        "[Mishapolk KKT refinements 2026-10-14]",
        "resources/web/mishapolk-kkt-refinements-2026-10-14/facts/n-304.yaml.gz",
        "70a033f0ecfa9e643cd5fb5dbac190cb7f4ffb94",
        "1792942775807517496548703186140836311278604266912137/100000000000000000000000000"
        "000000000000000000000000",
        _RUNZ7WN_B,
        "every view draws more light squares than the axis tool's view of this "
        "witness (2 or 4 to none): grid-slack's, admitted at row 10 at all three "
        "thresholds, and Evan Daniel's solved view, held at row 4 (solved above U); "
        "his same-side re-solve was refused (literal-too-large)",
        _README_R3CL,
    ),
    306: Settled(
        DECIDED,
        "[PingYou PR 574 certificates 2026-10-13]",
        "resources/web/pingyou-pr574-certificates-2026-10-13/facts/n-306.yaml.gz",
        "4c319c24a6217dbbbf05e79ebb7e2dc5be0a2cde",
        "297473394501716535450088605297944161012163039980988291424861242508494777555429"
        "146255284981684169305640512910756861163917877031400886942624530131089303691151"
        "587778784350086185785683086357285714951583876019780884868784352378328826891782"
        "689537265645869293538721550498267202299443174647030858757245338516898633049577"
        "994904161631590891290912829759252434277307944125780040223240353797563374872300"
        "920400934175893318506264139677344667082289210457637338370837808703753480678561"
        "319780253373722488639585652602989990615266502302937118053546261557379958136235"
        "277140337373352996726121602495664260728672383862692919636397478793168278361461"
        "18448929282630348382648623549134290095/165599405536848762386778997245769348161"
        "631750248152736945969472986946911663353865690197203056521392479411530333553555"
        "316987285384129093310819329199135669883212315631748890775635095278100905715543"
        "843519504796384142920417944642203440782640150587701434805076214281797537740651"
        "579407000889493180276721700757178493519035138830342820653681957477649888088734"
        "001005687301420224260693757600842764364722876640731097056894937838434820636841"
        "979019571628156237368723545591663157720743405519444602153922786824228326058320"
        "521066524659821082631697401282486026041894331926087540816929181936754823008442"
        "6091466458204363536274929507794187250417898151315185644790468268681051384162",
        _RUN3MRY,
        "Evan Daniel's solved view is held at row 4 (solved about 1e-19 above U), and "
        "grid-slack finds no view at 0.5, 1 or 5 degrees (relaxed rows overlap at this "
        "side)",
        _README_3MRY,
    ),
}


#: The counts allowed to stay `pending`, each naming the bead whose runs will decide it.
#: The list must equal the pending set, since `--check-state` fails on a pending count not
#: named here and on a named count that is no longer pending, so a count leaves it as soon
#: as a strong view is drawn or held or `SETTLED` decides its witness. It is also an input
#: to the state, not only a measure of it: a listed count reads pending even where its
#: house reads regular (`count_state`), since fourteen entries are the only record of a
#: strong view that lapsed before the index kept a `lapsed` block (review B1 of #641). So
#: two changes pass the gate and are the reviewer's to judge: dropping an entry whose count
#: then reads regular as published, which drops the runs its bead owes, and adding a count
#: whose house reads regular, which holds it pending; the pull request shows the bead's
#: runs or `--compare`'s table (review C2 of #641; think-k6rj). A count joins only by a
#: reviewed change naming its bead, and only for a witness corrected with its house's
#: source and exact side unchanged (`CORRECTED`): a count whose house moves never joins,
#: since its runs are owed in the pull request that moves it (`RUNS_OWED`), and
#: `deferral_problems` holds each entry to the base branch's record (`--base-ref`), so a
#: moved house fails whatever its entry declares (review C3 of #660).
#: Nothing stops a change adding entries, so the gate prints how many there are,
#: and `devtools.check_bead_tree` fails a change to this file whose list names a bead
#: that is not open (`deferrals`), so a bead named here is closed only once the change
#: taking its last count off has merged (regularization-process.md, "When a Witness
#: Changes"; review B4 of #636). Set on 15 October 2026 to the twenty counts the audit
#: found drawn without a strong generator's decision on their current witness
#: (think-gvke, think-rz8c). The nine of think-la7h (105, 129, 146, 156, 176, 204, 271,
#: 272 and 303) left it on 16 October 2026, six regularized and three decided, and so did
#: the eight of think-kpm3 (153, 154, 207, 211, 237, 241, 302 and 304), seven
#: regularized and one decided, and the three of think-3zi3 (175, 232 and 264), all
#: regularized, which left it empty. The adoption of 16 October 2026 (think-z7wn) allowed
#: eight re-housed counts under think-r3cl; its selection drew grid-slack's views at 232,
#: 264, 271 and 302 and decided 237, 303 and 304 the same day, and the owner's review
#: admitted Evan Daniel's view at 211, which row 7 had sent to review (review B3 of PR
#: 657; `regularized/reviews.yaml`), which left it empty again.
PENDING_ALLOWED: dict[int, str] = {}


def index_entries(index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """Every entry of the layer's index, by count."""
    document = json.loads(index.read_text(encoding="utf-8"))
    return {int(entry["n"]): entry for entry in document["entries"]}


def drawn_views(index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """The layer's entries that draw a view, by count."""
    return {
        n: entry for n, entry in index_entries(index).items() if entry["status"] == REGULARIZED
    }


def _view_witness(entry: Mapping[str, Any]) -> dict[str, Any]:
    text = gzip.decompress((REPO / entry["view"]["path"]).read_bytes()).decode("utf-8")
    return load_yaml(text)["witness"]


def drawn_above_bound(index: Path = INDEX) -> dict[int, float]:
    """Every drawn view whose exact side lies above `U`, by how far: each view's side read
    from its view file, exactly as both routes decide it, and held to `U` as the
    selection reads it."""
    from devtools import regularize_evand as drive  # noqa: PLC0415

    above: dict[int, float] = {}
    for n, entry in drawn_views(index).items():
        side, _placements, _corners = drive.view_geometry(_view_witness(entry))
        upper = drive.verified_bound(drive.case_facts(n))
        if upper is None:
            raise ValueError(f"n={n}: U is unknown")
        order = upper.compare(side)
        if order is None:
            raise ValueError(f"n={n}: U is not read exactly: {upper.unread}")
        if order > 0:
            above[n] = upper.difference(side)
    return above


def _routes(entry: Mapping[str, Any]) -> bool:
    """Whether both maintained exact routes accepted the view, as its entry records."""
    verdict = entry.get("exact_verification") or {}
    return bool(
        verdict.get("repository_verifier")
        and verdict.get("independent_checker")
        and verdict.get("passed")
    )


def _against(view: Fraction, house: Fraction | None) -> str | None:
    if house is None:
        return None
    return "smaller" if view < house else "larger" if view > house else "same"


def decide(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    """One count's view against its house drawing, and the picture the rule draws."""
    from devtools import regularize_select as select  # noqa: PLC0415

    tree, n, entries = unit
    return judged(n, entries[n], select.today((tree, n, entries)), select.today((tree, n, {})))


def judged(
    n: int, entry: Mapping[str, Any], view: Mapping[str, Any], house: Mapping[str, Any]
) -> dict[str, Any]:
    """`decide` on drawings already measured: the layer's view of count `n` (its index
    `entry`) and its house drawing, each as `regularize_select.today` measures it. The
    selection and admission read what the atlas draws from it too
    (`regularize_select.drawn`), so all three hold a view to the same picture."""
    from devtools import regularize_evand as drive  # noqa: PLC0415

    if view["drawing"]["kind"] != "regularized-view" or house["drawing"]["kind"] != "witness":
        raise ValueError(f"n={n}: the view and the house drawing were not both measured")
    side = Fraction(str(view["side"]))
    house_side = None if house["side"] is None else Fraction(str(house["side"]))
    upper = drive.verified_bound(drive.case_facts(n))
    order = None if upper is None else upper.compare(side)
    gains, worse = improvement_rule.compare(view, house)
    against = _against(side, house_side)
    judgement = improvement_rule.judge(
        gains,
        worse,
        smaller=against == "smaller",
        larger=against == "larger",
        # Exactness is the gain of an exactly verified view over a numerically checked
        # witness, so a view an exact route refused gains none (review B2 of #591).
        exact_gain=not house["verified"] and _routes(entry),
    )
    if not _routes(entry):
        default, reason = HOUSE, ROUTE_REFUSED
    elif order is None:
        default, reason = HOUSE, UNKNOWN_U
    elif order > 0 and n not in ABOVE_U:
        default, reason = HOUSE, ABOVE_BOUND
    elif not judgement.improves:
        default, reason = HOUSE, judgement.reason
    else:
        default, reason = REGULARIZED, f"better on {', '.join(judgement.better)}"
    return {
        "n": n,
        "default": default,
        "reason": reason,
        "generator": entry.get("generator"),
        "view": entry["view"]["path"],
        "exact_routes": _routes(entry),
        "side": {
            "view_minus_U": None
            if upper is None or order is None
            else f"{upper.difference(side):.3e}",
            "named_above_U": n in ABOVE_U,
            "against_house": against,
        },
        "house_exact": bool(house["verified"]),
        "better": list(judgement.better),
        "worse": list(judgement.worse),
        "measures": {key: {"view": view[key], "house": house[key]} for key in MEASURES},
    }


def measure_house(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    """One count's house drawing, measured as `decide` measures it, where the layer draws
    no view: the measures its regularization state is read from."""
    from devtools import regularize_select as select  # noqa: PLC0415

    tree, n, _entries = unit
    house = select.today((tree, n, {}))
    if house["drawing"]["kind"] != "witness":
        raise ValueError(f"n={n}: the house drawing was not measured")
    return {"n": n, "measures": {key: house[key] for key in MEASURES}}


def _text(value: object) -> str | None:
    return None if value is None else str(value)


def witness_identity(tree: Path, entry: Mapping[str, Any]) -> dict[str, str | None]:
    """The witness a count's index entry names, as it identifies itself: its id, its
    source's key, path and revision, and its side, as written. A state is bound to the
    last four, never to a digest of the file's bytes (OR-16): a new house changes the
    source, a new certificate file the path, an upstream fix the revision. The id is the
    count's (`W-known-best-nNNN`) and stays the same across houses."""
    witness = load_yaml((tree / entry["source"]["witness"]).read_text(encoding="utf-8"))[
        "witness"
    ]
    source = witness.get("source") or {}
    return {
        "id": str(witness["id"]),
        "source": _text(source.get("key")),
        "path": _text(source.get("path")),
        "revision": _text(source.get("revision")),
        "side": str(witness["side"]),
    }


def _measure(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    """One count measured: `decide` where the layer draws a view, else `measure_house`."""
    _tree, n, entries = unit
    return {"n": n, "measured": decide(unit) if n in entries else measure_house(unit)}


def _axis_record(entry: Mapping[str, Any]) -> Mapping[str, Any]:
    """The axis tool's own record of a count: the entry, or its `reference` where another
    generator's view is the entry."""
    return entry.get("reference") or entry


def _axis_outcome(record: Mapping[str, Any]) -> str:
    status = str(record["status"])
    if status == "refused":
        return f"refused: {record['refusal']['kind']}"
    return {"regularized": "view", "unchanged": "no change"}.get(status, status)


#: The fields a witness identifies itself by and a `SETTLED` entry is bound to. A source
#: that pins no revision binds by key and side alone where its path is a shared index:
#: every Kingbird witness names `sources.json`, so the exemptions at 39, 55, 290 and 291
#: bind to the source key and the side, and 290 and 291 to the same pair. Binding its
#: `url` and `retrieved` as well changes the record, a data commit (think-k09z; review
#: B5 of #636).
IDENTITY = ("source", "path", "revision", "side")


def _settled_here(held: Settled | None, witness: Mapping[str, Any]) -> Settled | None:
    """A `SETTLED` entry where it was made on this witness: its source's key, path and
    revision, and its side."""
    if held is None or any(getattr(held, key) != witness.get(key) for key in IDENTITY):
        return None
    return held


def run_decisions(
    entry: Mapping[str, Any], settled: Settled | None, held: str | None = None
) -> list[dict[str, Any]]:
    """The tool runs that decided a count's current witness, and what each found: the axis
    tool's record and the strong generator whose view the layer holds, both of the
    witness the atlas holds (`--check-atlas` holds the index to it), and a `SETTLED`
    entry's runs where it was made on that witness. A strong view the rule does not draw
    reads `held: ` and why (`held`), not `view` (review B3 of #636)."""
    axis = _axis_record(entry)
    found: list[dict[str, Any]] = [
        {"generator": ALGORITHM, "run": None, "outcome": _axis_outcome(axis)}
    ]
    if entry.get("generator") != ALGORITHM:
        outcome = "view" if held is None else f"held: {held}"
        found.append(
            {
                "generator": entry["generator"],
                "run": str(entry["run"]["id"]),
                "outcome": outcome,
            }
        )
    if settled is not None:
        found.extend(
            {"generator": generator, "run": run, "outcome": settled.outcome}
            for generator, run in settled.runs
        )
    return found


def count_state(
    n: int,
    entry: Mapping[str, Any],
    decided: Mapping[str, Any],
    witness: Mapping[str, Any],
    *,
    settled: Mapping[int, Settled] | None = None,
    allowed: Mapping[int, str] | None = None,
) -> dict[str, Any]:
    """One count's regularization state, from its index entry, what `decide` or
    `measure_house` measured (`decided`), and its witness as it identifies itself
    (`witness_identity`); the module's docstring gives the states."""
    settled = SETTLED if settled is None else settled
    allowed = PENDING_ALLOWED if allowed is None else allowed
    viewed = decided.get("default") == REGULARIZED
    measures = decided["measures"]
    house = (
        {key: value[HOUSE] for key, value in measures.items()}
        if "default" in decided
        else dict(measures)
    )
    drawn = {key: value[VIEW] for key, value in measures.items()} if viewed else house
    generator = str(entry["generator"]) if viewed else None
    current = _settled_here(settled.get(n), witness)
    lapse = entry.get(LAPSED) if entry.get("generator") == ALGORITHM else None
    if generator in STRONG_GENERATORS:
        state = REGULARIZED_STATE
        why = f"the {generator} view of this witness is drawn (run {entry['run']['id']})"
    elif (
        lapse is None
        and n not in allowed
        and house["uneven_axis"] == 0
        and house["near_axis"] == 0
    ):
        # A lapse comes first: a strong view drew this count on an earlier witness and
        # nothing has decided this one, so a regular house does not settle it (review B2
        # of #636: 13 of the counts a strong view regularizes have a regular house, and
        # at 230 the drawing fell from 626 full shared sides to 562 with the gate green).
        # Only here does the state read the block; elsewhere it only explains a pending
        # count, so a hand merge that drops it falls back to this branch, never further.
        # So does the allowlist (review B1 of #641): fourteen of its first entries record a
        # strong view that lapsed before `--update-atlas` wrote the block (272's and 304's
        # Evan Daniel views were never admitted to the index at all), so their records
        # carry none. A regular new house would read regular, the gate would ask for the
        # entry to come off, and the runs its bead owes would be dropped; on the list, a
        # count waits for them.
        state = REGULAR_AS_PUBLISHED
        why = "the house drawing has no uneven and no near-axis square"
    elif entry.get("generator") in STRONG_GENERATORS:
        # The layer holds a strong generator's view of this witness, and the improvement
        # rule does not draw it: that generator decided the witness, and drew no better.
        state = DECIDED
        why = (
            f"the {entry['generator']} view of this witness (run {entry['run']['id']}) is "
            f"not drawn: {decided['reason']}"
        )
    elif current is not None:
        state = current.state
        why = f"{current.outcome} ({current.evidence})"
        if current.owed:
            why += f"; still owed: {current.owed}"
    else:
        state = PENDING
        what = f"the {generator} view" if viewed else "the house drawing"
        why = f"no strong generator has decided this witness; {what} is drawn"
        if lapse:
            # The last strong view that lapsed here, which may be more than one house
            # back: `--update-atlas` carries it until a strong view is admitted again.
            why += (
                f"; the {lapse['generator']} view of an earlier witness lapsed "
                f"(run {lapse['run']})"
            )
        if n in allowed:
            why += f"; allowed pending: {allowed[n]}"
    return {
        "n": n,
        "state": state,
        "drawn": VIEW if viewed else HOUSE,
        "generator": generator,
        "witness": dict(witness),
        "measures": drawn,
        "decisions": run_decisions(
            entry, current, held=None if viewed else decided.get("reason")
        ),
        "lapsed": lapse,
        "why": why,
    }


def _identify(unit: tuple[Path, Mapping[str, Any]]) -> dict[str, str | None]:
    tree, entry = unit
    return witness_identity(tree, entry)


def document(*, workers: int = 1, tree: Path = REPO, index: Path = INDEX) -> dict[str, Any]:
    """The record the data gives: every drawn view's count decided, and every count's
    regularization state."""
    every = index_entries(index)
    entries = {n: entry for n, entry in every.items() if entry["status"] == REGULARIZED}
    units = [(tree, n, entries) for n in sorted(every, reverse=True)]
    named = [(tree, every[n]) for n in sorted(every)]
    if workers > 1 and len(units) > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            measured = list(pool.map(_measure, units))
            identities = list(pool.map(_identify, named))
    else:
        measured = [_measure(unit) for unit in units]
        identities = [_identify(unit) for unit in named]
    by_n = {int(row["n"]): row["measured"] for row in measured}
    witnesses = dict(zip(sorted(every), identities, strict=True))
    rows = [by_n[n] for n in sorted(entries)]
    states = [count_state(n, every[n], by_n[n], witnesses[n]) for n in sorted(every)]
    drawn = sum(1 for row in rows if row["default"] == REGULARIZED)
    return {
        "softschema": {"contract": CONTRACT, "schema": SCHEMA, "status": "enforced"},
        "contract": CONTRACT,
        "generated_by": f"{GENERATOR} --update",
        "policy_document": improvement_rule.POLICY_DOCUMENT,
        "rule": improvement_rule.SECTION,
        "measured_by": (
            "devtools.regularize_select.today on the view and on the house witness, "
            "judged by devtools.improvement_rule.judge"
        ),
        "measures": list(MEASURES),
        "totals": {
            "views": len(rows),
            REGULARIZED: drawn,
            HOUSE: len(rows) - drawn,
            "states": {
                state: sum(1 for row in states if row["state"] == state) for state in STATES
            },
        },
        "entries": rows,
        "states": states,
    }


def text(record: Mapping[str, Any]) -> str:
    return retained_json.dumps(record, ensure_ascii=False) + "\n"


@cache
def decisions(record: Path = RECORD, index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """Every drawn view's decision, by count, from the retained record, refused where the
    record's counts, views or generators are not the index's: a stale record is refused
    rather than drawn from. Nothing is measured here; the records tier's check measures."""
    stale = f"{RECORD_PATH} is stale; run `{GENERATOR} --update`"
    found = json.loads(record.read_text(encoding="utf-8"))
    if found.get("contract") != CONTRACT:
        raise SystemExit(f"{RECORD_PATH} is not a {CONTRACT} record")
    drawn = drawn_views(index)
    rows = {int(row["n"]): row for row in found["entries"]}
    if sorted(rows) != sorted(drawn):
        raise SystemExit(f"{stale}: it decides other counts than the index draws")
    for n, row in rows.items():
        if row["view"] != drawn[n]["view"]["path"] or row["generator"] != drawn[n].get(
            "generator"
        ):
            raise SystemExit(f"{stale}: n={n} names another view than the index")
    return rows


@cache
def regularized_defaults(
    record: Path = RECORD, index: Path = INDEX
) -> dict[int, dict[str, Any]]:
    """The counts whose default picture is their regularized view (`decisions`)."""
    rows = decisions(record, index)
    return {n: row for n, row in rows.items() if row["default"] == REGULARIZED}


def held_reasons(record: Path = RECORD) -> dict[str, str]:
    """By view path, why each view the layer holds is not its count's default picture, in
    the words a case record's note gives it (review A4 of #591): the record's reason, or
    for a tie, that it ties the house drawing on every goal. Read from the retained record
    without measuring, and by the view's path, so a view the record does not name gets no
    reason here (`regularized_drawings.case_note`). A goal it is worse on is named in the
    policy's words (`improvement_rule.GOAL_NAMES`), never as the code's key: the n = 176
    note read "worse on uneven_axis" (review A9 of #636)."""
    found = json.loads(record.read_text(encoding="utf-8"))
    return {
        str(row["view"]): _held_words(row)
        for row in found.get("entries") or []
        if row["default"] == HOUSE
    }


def _worse_words(goal: str) -> str:
    """What being worse on one goal of the improvement rule draws, in a reader's words."""
    name = improvement_rule.GOAL_NAMES[goal]
    if goal in improvement_rule.FEWER_IS_BETTER:
        return f"more {name}"
    if goal == improvement_rule.SIDE:
        return f"a larger {name}"
    return f"a smaller {name}"


def _held_words(row: Mapping[str, Any]) -> str:
    """Why a held view is not drawn, as a case record's note says it."""
    if row["reason"] == "no gain":
        return "it ties the house drawing on every goal of the improvement rule"
    if row["worse"] and row["reason"].startswith("worse on "):
        return "it draws " + ", ".join(_worse_words(str(goal)) for goal in row["worse"])
    return str(row["reason"])


@cache
def _generators(index: Path = INDEX) -> dict[str, Any]:
    return dict(json.loads(index.read_text(encoding="utf-8")).get("generators") or {})


def credit_line(n: int) -> str:
    """The credit line a drawing of count `n`'s regularized default carries: the
    generator's, as the policy's section 7 gives it (`regularized_drawings.
    generator_credit`)."""
    from devtools.regularized_drawings import generator_credit  # noqa: PLC0415

    row = regularized_defaults()[n]
    return generator_credit(str(row["generator"]), _generators())


def problems(expected: Mapping[str, Any], record: Path = RECORD) -> tuple[list[str], list[str]]:
    """What fails the check, and what it lists without failing: the counts that keep
    the house picture and why."""
    found = list(improvement_rule.problems())
    by_n = {int(row["n"]): row for row in expected["entries"]}
    if not record.is_file():
        found.append(f"{RECORD_PATH} is missing")
    else:
        retained = json.loads(record.read_text(encoding="utf-8"))
        for row in retained.get("entries", []):
            n = int(row["n"])
            if row.get("default") == REGULARIZED and by_n.get(n, {}).get("default") != (
                REGULARIZED
            ):
                why = by_n[n]["reason"] if n in by_n else "the index draws no view"
                found.append(
                    f"n={n} is drawn regularized by default, and the rule says not: {why}"
                )
        if record.read_text(encoding="utf-8") != text(expected):
            found.append(f"{RECORD_PATH} is not what the data gives")
    kept = [
        f"n={row['n']} keeps the house picture: {row['reason']}"
        for row in expected["entries"]
        if row["default"] == HOUSE
    ]
    return found, kept


def _summary(record: Mapping[str, Any]) -> str:
    totals = record["totals"]
    return (
        f"{totals[REGULARIZED]} of {totals['views']} drawn views are their counts' default "
        f"pictures, each improving on its house drawing; {totals[HOUSE]} keep the house"
    )


def _states_summary(rows: Sequence[Mapping[str, Any]]) -> str:
    counts = {state: sum(1 for row in rows if row["state"] == state) for state in STATES}
    return f"{len(rows)} counts: " + ", ".join(
        f"{counts[state]} {state.replace('-', ' ')}" for state in STATES
    )


def state_problems(
    record: Path = RECORD,
    index: Path = INDEX,
    *,
    settled: Mapping[int, Settled] | None = None,
    allowed: Mapping[int, str] | None = None,
    evidence: Path = EVIDENCE,
    corrected: Mapping[int, Correction] | None = None,
    base: Base | None = None,
) -> tuple[list[str], list[str]]:
    """What fails the regularization-state gate, and the pending counts it lists: the
    retained record against the index, `SETTLED` and `PENDING_ALLOWED`, and each deferral
    against the witness it defers, held to `base` where one is given
    (`deferral_problems`), nothing measured and no witness read (`--check` holds the
    record to the data by deciding it again)."""
    settled = SETTLED if settled is None else settled
    allowed = PENDING_ALLOWED if allowed is None else allowed
    found = json.loads(record.read_text(encoding="utf-8"))
    if found.get("contract") != CONTRACT:
        return [f"{RECORD_PATH} is not a {CONTRACT} record"], []
    stale = f"run `{GENERATOR} --update`"
    every = index_entries(index)
    recorded = run_records(index, evidence)
    rows = {int(row["n"]): row for row in found.get("states") or []}
    problems: list[str] = []
    if sorted(rows) != sorted(every) or len(rows) != len(found.get("states") or []):
        problems.append(
            f"{RECORD_PATH}'s states are not the index's counts, once each; {stale}"
        )
    for n in sorted(set(rows) & set(every)):
        row, entry = rows[n], every[n]
        witness = row.get("witness") or {}
        # The id is the count's, the same for every house it has had, so this holds the
        # row to its count; a new house is the SETTLED comparison's to catch below, and a
        # record older than its witness the measuring `--check`'s.
        if witness.get("id") != entry["source"]["id"]:
            problems.append(
                f"n={n}: the record's row names witness {witness.get('id')!r}, and the "
                f"index's count names {entry['source']['id']!r}; {stale}"
            )
        if row["state"] not in STATES:
            problems.append(f"n={n}: state {row['state']!r}")
        if row["drawn"] == VIEW and row["generator"] != entry.get("generator"):
            problems.append(
                f"n={n}: the record draws another view than the index holds; {stale}"
            )
        held = settled.get(n)
        if held is not None:
            problems.extend(_settled_problems(n, held, row, entry, recorded))
    problems.extend(
        f"{EVIDENCE_PATH}{SETTLED_RUNS}/{run}/run.json is not the copy of a run a "
        "SETTLED entry names; delete it with the settlement it was retained for"
        for run in orphaned_copies(evidence, settled=settled)
    )
    problems.extend(_list_problems(rows, allowed))
    problems.extend(deferral_problems(rows, allowed, corrected=corrected, base=base))
    pending = {n for n, row in rows.items() if row["state"] == PENDING}
    listed = [
        f"n={n} is pending, allowed: {allowed[n]}" for n in sorted(pending & set(allowed))
    ]
    summary = f"regularization states: {_states_summary(list(rows.values()))}"
    return problems, [*listed, f"PENDING_ALLOWED: {len(allowed)} counts", summary]


class RunRecord(NamedTuple):
    """What the records say of one run: its generator; whether the retained evidence
    holds it, rather than the layer's index alone; and the counts it covered, where a
    record lists them (`None` where none does, as an index block, which keeps only how
    many)."""

    generator: str
    retained: bool
    counts: frozenset[int] | None


def run_records(index: Path = INDEX, evidence: Path = EVIDENCE) -> dict[str, RunRecord]:
    """Every run a record holds, by id: the layer index's run blocks, and in the retained
    evidence each run's block (`run.json`, which a grid-slack run's retained reports are
    summed into, or a block `--retain-runs` copied from the index) and each driver run's
    `receipt.json`, which records no id: the driver names a run
    `evand-regularize-<run directory>` (`regularize_evand.record_rungs`). A receipt lists
    the counts its run covered; beside a block, the counts with a retained report are
    the ones it covered, and a copied block has none."""
    document = json.loads(index.read_text(encoding="utf-8"))
    generators = {
        str(block["id"]): str(block["generator"]) for block in document.get("runs") or []
    }
    retained: dict[str, set[int] | None] = {}

    def hold(run: str, generator: str, counts: set[int] | None) -> None:
        generators.setdefault(run, generator)
        known = retained.get(run)
        retained[run] = known if counts is None else counts | (known or set())

    for path in sorted(evidence.glob("*/*/run.json")):
        block = json.loads(path.read_text(encoding="utf-8"))
        reports = {
            int(report.parent.name.removeprefix("n-"))
            for pattern in ("n-*/report.json", "n-*/report.json.gz")
            for report in path.parent.glob(pattern)
        }
        hold(str(block["id"]), str(block["generator"]), reports or None)
    for path in sorted(evidence.glob("*/*/receipt.json")):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        directory = str(receipt.get("run_directory") or path.parent.name)
        counts = {int(count["n"]) for count in receipt.get("counts") or []}
        hold(f"{EVAND_GENERATOR}-{directory}", EVAND_GENERATOR, counts or None)
    return {
        run: RunRecord(
            generator,
            run in retained,
            None if (counts := retained.get(run)) is None else frozenset(counts),
        )
        for run, generator in generators.items()
    }


def recorded_runs(index: Path = INDEX, evidence: Path = EVIDENCE) -> dict[str, str]:
    """Every run a record holds, as {run id: generator} (`run_records`)."""
    return {run: record.generator for run, record in run_records(index, evidence).items()}


def orphaned_copies(
    evidence: Path = EVIDENCE, *, settled: Mapping[int, Settled] | None = None
) -> list[str]:
    """The runs whose index block `--retain-runs` copied into `SETTLED_RUNS` that no
    `SETTLED` entry names any longer, by the copy's directory and the block's own id, so
    a copy whose directory and id disagree is listed too (review G2 of #644)."""
    settled = SETTLED if settled is None else settled
    named = {run for held in settled.values() for _generator, run in held.runs}
    orphans: list[str] = []
    for path in sorted((evidence / SETTLED_RUNS).glob("*/run.json")):
        block = json.loads(path.read_text(encoding="utf-8"))
        if path.parent.name not in named or str(block.get("id")) != path.parent.name:
            orphans.append(path.parent.name)
    return orphans


def retain_runs(
    index: Path = INDEX,
    evidence: Path = EVIDENCE,
    *,
    settled: Mapping[int, Settled] | None = None,
) -> tuple[list[str], list[str]]:
    """Copy into the evidence (`SETTLED_RUNS`) the layer index's block of each run a
    `SETTLED` entry names that the evidence does not hold yet, as the index has it, so
    the settlement keeps its record after the index drops the block. Returns the runs
    written and the runs no record holds, which nothing here can retain."""
    settled = SETTLED if settled is None else settled
    records = run_records(index, evidence)
    blocks = {
        str(block["id"]): block
        for block in json.loads(index.read_text(encoding="utf-8")).get("runs") or []
    }
    named = sorted({run for held in settled.values() for _generator, run in held.runs})
    written: list[str] = []
    missing: list[str] = []
    for run in named:
        if run in records and records[run].retained:
            continue
        if run not in blocks:
            missing.append(run)
            continue
        target = evidence / SETTLED_RUNS / run / "run.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(target) as temporary:
            temporary.write_text(
                retained_json.dumps(blocks[run], ensure_ascii=False), encoding="utf-8"
            )
        written.append(run)
    return written, missing


def _settled_problems(
    n: int,
    held: Settled,
    row: Mapping[str, Any],
    entry: Mapping[str, Any],
    recorded: Mapping[str, RunRecord],
) -> list[str]:
    """What is wrong with one `SETTLED` entry against the record's row, the index and
    the runs a record holds (`run_records`)."""
    witness = row.get("witness") or {}
    problems: list[str] = []
    for generator, run in held.runs:
        found = recorded.get(run)
        if found is None:
            problems.append(
                f"n={n}: SETTLED names run {run}, which no record holds: neither the "
                f"layer's index nor a run block or receipt under {EVIDENCE_PATH}; retain "
                "its evidence or take it off"
            )
            continue
        if found.generator != generator:
            problems.append(
                f"n={n}: SETTLED names run {run} as {generator}'s, and its record as "
                f"{found.generator}'s"
            )
        if not found.retained:
            problems.append(
                f"n={n}: SETTLED names run {run}, which only the layer's index holds, and "
                "the index drops a run's block once no entry draws from it; run "
                f"`{GENERATOR} --retain-runs` to keep the block under {EVIDENCE_PATH}"
            )
        elif found.counts is not None and n not in found.counts:
            problems.append(
                f"n={n}: SETTLED names run {run}, whose record shows it ran "
                f"{', '.join(str(count) for count in sorted(found.counts))}, not {n}"
            )
    if _settled_here(held, witness) is None:
        moved = ", ".join(
            f"{key} {str(getattr(held, key))[:24]!r} to {str(witness.get(key))[:24]!r}"
            for key in IDENTITY
            if getattr(held, key) != witness.get(key)
        )
        problems.append(
            f"n={n}: SETTLED was decided on another witness ({moved}); run the generators "
            'on it (regularization-process.md, "When a Witness Changes"), then settle it '
            "again or take it off SETTLED"
        )
    elif row["state"] in (REGULARIZED_STATE, REGULAR_AS_PUBLISHED):
        problems.append(f"n={n}: SETTLED names it, but it is {row['state']}; take it off")
    elif entry.get("generator") in STRONG_GENERATORS:
        problems.append(
            f"n={n}: SETTLED names it, but the layer holds the {entry['generator']} view of "
            "this witness, which decides it unaided; take it off"
        )
    if held.state not in (DECIDED, OWED, EXEMPT):
        problems.append(f"n={n}: SETTLED gives state {held.state!r}")
    if held.state == EXEMPT and not BEAD.search(held.evidence):
        problems.append(f"n={n}: an exemption names the bead that owns it")
    if held.state == OWED and held.owed is None:
        problems.append(f"n={n}: a regularization owed names the bead that owes it in `owed`")
    if held.owed is not None and not BEAD.match(held.owed):
        problems.append(f"n={n}: SETTLED's owed names no bead first: {held.owed!r}")
    return problems


def _list_problems(
    rows: Mapping[int, Mapping[str, Any]], allowed: Mapping[int, str]
) -> list[str]:
    """Where the pending set and `PENDING_ALLOWED` differ, and an entry naming no bead."""
    pending = {n for n, row in rows.items() if row["state"] == PENDING}
    problems = [
        f"n={n} is pending: {rows[n]['why']}. Run the strong generators on its witness "
        '(regularization-process.md, "When a Witness Changes"), or allow it in '
        "PENDING_ALLOWED with the bead that owns the run"
        for n in sorted(pending - set(allowed))
    ]
    problems.extend(
        f"n={n}: PENDING_ALLOWED names it, but it is "
        f"{rows[n]['state'] if n in rows else 'not a count'}; take it off the list"
        for n in sorted(set(allowed) - pending)
    )
    problems.extend(
        f"n={n}: PENDING_ALLOWED names no bead: {allowed[n]!r}"
        for n in sorted(allowed)
        if not BEAD.match(allowed[n])
    )
    return problems


class Correction(NamedTuple):
    """A deferral made since the house rule (`select_houses.RULE_SET_ON`): the witness the
    correction replaced, as the base branch's record names it, by its source's key, path
    and revision and its exact side. The corrected witness, the record's, keeps that
    source and that exact side and is another witness only (review C3 of #660)."""

    source: str
    path: str | None
    revision: str | None
    side: str


class Base(NamedTuple):
    """The record a change is held to (`base_record`): the base branch's rows by count, and
    the counts whose witness file the change alters, which is how a correction shows at a
    source that pins no revision, as Kingbird's catalogue and the grid do not."""

    ref: str
    rows: Mapping[int, Mapping[str, Any]]
    changed: frozenset[int]


#: The deferrals made since the rule: a witness corrected or re-solved with its house's
#: source and exact side unchanged, whose runs wait for the bead its `PENDING_ALLOWED`
#: entry names (packing/campaign/result-import.md, "Adopt a House, Then Regularize It").
#: The twenty deferrals the list held when the owner set the rule were each run or decided
#: by 16 October 2026 (#644, #653, #654 and #657), so every entry since is one of these.
CORRECTED: dict[int, Correction] = {}

#: Where the house witnesses are, one file a count, as the index names them.
WITNESSES_PATH = "packing/witnesses/known-best"
_WITNESS_FILE = re.compile(r"(?:.*/)?n-(\d+)\.yaml")


def _git(*arguments: str) -> str:
    import subprocess  # noqa: PLC0415

    done = subprocess.run(
        ["git", "-C", str(REPO), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if done.returncode != 0:
        detail = done.stderr.strip() or f"exit {done.returncode}"
        raise SystemExit(f"git {' '.join(arguments)}: {detail}")
    return done.stdout


#: What a clone without its merge base is told: AGENTS.md's fresh-clone steps fetch the
#: history a shallow session clone lacks.
UNSHALLOW = (
    "the clone is shallow, so the merge base of {ref} and HEAD is not in it; run "
    '`git fetch --unshallow` (AGENTS.md, "A fresh clone") and check again'
)


def base_record(ref: str) -> Base:
    """The record of the commit this change is built on, from `ref`: its merge base with
    `HEAD`, so a branch that has not merged `ref`'s latest commits is held to the record
    it started from, and the counts whose witness file differs here from that commit's.

    It reads the base branch's copy of the record as the release-impact and changelog
    gates read theirs (OR-18): the base is no recorded revision, and without it the gate
    fails closed, naming the remedy where the clone is shallow (review D5 of #660)."""
    try:
        _git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    except SystemExit as error:
        raise SystemExit(f"--base-ref {ref} names no commit in this clone; fetch it") from error
    try:
        commit = _git("merge-base", ref, "HEAD").strip()
    except SystemExit as error:
        if _git("rev-parse", "--is-shallow-repository").strip() == "true":
            raise SystemExit(UNSHALLOW.format(ref=ref)) from error
        raise
    document = json.loads(_git("show", f"{commit}:{RECORD_PATH}"))
    rows = {int(row["n"]): row for row in document.get("states") or []}
    names = _git("diff", "--name-only", commit, "--", WITNESSES_PATH).split()
    changed = frozenset(
        int(match.group(1)) for name in names if (match := _WITNESS_FILE.fullmatch(name))
    )
    return Base(ref, rows, changed)


def _short(side: object) -> str:
    """A side as a message names it: its first sixteen decimals."""
    try:
        value = Fraction(str(side))
    except ValueError, ZeroDivisionError:
        return repr(side)
    return f"{float(value):.16g}"


def _same_side(first: object, second: object) -> bool:
    """Whether two sides as the record writes them are one number exactly."""
    try:
        return Fraction(str(first)) == Fraction(str(second))
    except ValueError, ZeroDivisionError:
        return str(first) == str(second)


def _identity(witness: Mapping[str, Any]) -> tuple[str | None, ...]:
    """A witness as it identifies itself (`IDENTITY`), each field as the record writes it."""
    return tuple(None if witness.get(key) is None else str(witness[key]) for key in IDENTITY)


def _deferred_in(row: Mapping[str, Any] | None) -> bool:
    """Whether a record's row is a pending count `PENDING_ALLOWED` allowed, which the record
    copies into its reason (`count_state`)."""
    return (
        row is not None
        and row.get("state") == PENDING
        and "; allowed pending: " in str(row.get("why"))
    )


def _correction_problems(
    n: int, fix: Correction, witness: Mapping[str, Any], base: Base | None
) -> list[str]:
    """What fails a `CORRECTED` entry, held to the base record where there is one."""
    source, side = str(witness.get("source")), str(witness.get("side"))
    if fix.source != source or not _same_side(fix.side, side):
        return [
            (
                f"n={n}: CORRECTED says the correction replaced the witness from {fix.source} "
                f"at {_short(fix.side)}, and the record's is from {source} at {_short(side)}: "
                "a correction keeps its house's source and exact side, and where the house "
                "moved, by any import, its runs are owed in the pull request that moved it"
            )
        ]
    if base is None:
        # Declared only: `--check-state --base-ref` holds it to the base record.
        own = (fix.source, fix.path, fix.revision, fix.side) == _identity(witness)
        if own and fix.revision is not None:
            return [
                (
                    f"n={n}: CORRECTED names the record's own witness as the one it replaced: "
                    "there is no corrected witness to defer"
                )
            ]
        return []
    return _base_problems(n, fix, witness, base)


def _base_problems(
    n: int, fix: Correction, witness: Mapping[str, Any], base: Base
) -> list[str]:
    """What fails a `CORRECTED` entry against the base record (reviews C3 and D1 of #660).

    Where the base already defers the count, the correction was held to its own base when
    it was made, and it stands while the record's witness keeps the base's source and
    exact side, whatever a later change does to its file or path. Otherwise this change
    makes the correction: the entry names the base's witness, and the record's is another
    witness, by its path or revision, or, at a source that pins no revision, by its file.
    """
    row = base.rows.get(n)
    before = (row or {}).get("witness") or {}
    if _deferred_in(row):
        if str(before.get("source")) == str(witness.get("source")) and _same_side(
            before.get("side"), witness.get("side")
        ):
            return []
        return [
            (
                f"n={n}: {base.ref}'s record defers it at the witness from "
                f"{before.get('source')} at {_short(before.get('side'))}, and the house "
                "has moved since: its runs are owed in the pull request that moved it"
            )
        ]
    if _identity(before) != (fix.source, fix.path, fix.revision, fix.side):
        return [
            (
                f"n={n}: CORRECTED says the correction replaced the witness from {fix.source} "
                f"at {_short(fix.side)} ({fix.path}, revision {fix.revision}), but "
                f"{base.ref}'s record names {before.get('source')} at "
                f"{_short(before.get('side'))} ({before.get('path')}, revision "
                f"{before.get('revision')}): it names the witness the base holds"
            )
        ]
    revisionless = witness.get("revision") is None
    if _identity(before) == _identity(witness) and not (revisionless and n in base.changed):
        return [
            (
                f"n={n}: CORRECTED names {base.ref}'s witness as the one it replaced, and the "
                "record's is that witness: there is no corrected witness to defer (a "
                "changed file shows a correction only where the source pins no revision)"
            )
        ]
    return []


def deferral_problems(
    rows: Mapping[int, Mapping[str, Any]],
    allowed: Mapping[int, str],
    *,
    corrected: Mapping[int, Correction] | None = None,
    base: Base | None = None,
) -> list[str]:
    """Where `PENDING_ALLOWED` defers the runs of a witness it may not.

    Since the house rule a count's runs wait only for a witness corrected or re-solved
    with its house's source and exact side unchanged, and never because its house moved,
    whichever import moved it (reviews A5, B1, B2, C3 and D1 of #660). Each entry is a
    `CORRECTED` one, which names the witness it replaced. Against the base record
    (`base_record`), that witness is the base's at the same count, the record's has its
    source and exact side, and it is another witness only: another path or revision, or,
    at a source that pins no revision, another file. A house moved by an adoption, a
    catalogue intake or a re-solve fails, whatever the entry says. An entry the base
    already defers was held to its own base when it was made, and stands while the
    record's witness keeps the base's source and exact side. Without a base the entry is
    checked as declared.
    """
    from devtools.select_houses import RULE_SET_ON  # noqa: PLC0415

    corrected = CORRECTED if corrected is None else corrected
    problems: list[str] = []
    for n in sorted(allowed):
        witness = (rows.get(n) or {}).get("witness") or {}
        fix = corrected.get(n)
        if fix is None:
            problems.append(
                f"n={n}: PENDING_ALLOWED defers its runs, but CORRECTED names no corrected "
                f"witness there: since the owner set the house rule ({RULE_SET_ON}), a "
                "count whose house moves is regularized in the pull request that moves it"
            )
            continue
        problems.extend(_correction_problems(n, fix, witness, base))
    problems.extend(
        f"n={n}: CORRECTED names it, but PENDING_ALLOWED does not; take it off"
        for n in sorted(set(corrected) - set(allowed))
    )
    return problems


def deferrals(
    settled: Mapping[int, Settled] | None = None, allowed: Mapping[int, str] | None = None
) -> list[tuple[str, str]]:
    """Every bead this module defers regularization work to, as (where, the bead alias),
    for `devtools.check_bead_tree`'s dead-deferral check: each count `PENDING_ALLOWED`
    names, each exemption's owning bead and each decision's `owed` bead. Whether one is
    named at all is `--check-state`'s to hold; this asks only whether it is still open."""
    settled = SETTLED if settled is None else settled
    allowed = PENDING_ALLOWED if allowed is None else allowed
    where = "default_drawings.py"
    named = [
        (f"{where} PENDING_ALLOWED n={n}", found[0])
        for n, why in sorted(allowed.items())
        if (found := BEAD.match(why))
    ]
    for n, held in sorted(settled.items()):
        if held.state == EXEMPT and (found := BEAD.search(held.evidence)):
            named.append((f"{where} SETTLED n={n} exempt", found[0]))
        if held.owed is not None and (found := BEAD.match(held.owed)):
            named.append((f"{where} SETTLED n={n} owed", found[0]))
    return named


#: The words `--check-state --base-ref` prints, which the records tier's step requires,
#: so a step that stops passing the base fails (review D4 of #660).
HELD_TO_BASE = "CORRECTED is held to the record at the merge base of"


def check_state(base_ref: str | None = None) -> int:
    # The base is read only where a count is deferred, so a clone without the merge base
    # passes while nothing is (review D5 of #660).
    deferring = bool(PENDING_ALLOWED or CORRECTED)
    base = base_record(base_ref) if base_ref is not None and deferring else None
    found, listed = state_problems(base=base)
    if base_ref is None:
        listed.append("CORRECTED is checked as declared: no --base-ref to hold it to")
    elif base is None:
        listed.append(f"{HELD_TO_BASE} {base_ref}; nothing is deferred, so none was read")
    else:
        listed.append(f"{HELD_TO_BASE} {base_ref}")
    for line in listed:
        print(line)
    if found:
        for problem in found:
            print(f"regularization state: {problem}")
        return 1
    print(
        "regularization state check passed: every count is regularized, regular as "
        "published, decided, owed to an open bead or exempt, or pending and named in "
        "PENDING_ALLOWED, which equals the pending set and grows only by a reviewed change "
        "naming its bead"
    )
    return 0


def retain() -> int:
    written, missing = retain_runs()
    for run in written:
        print(f"retained run {run}'s block in {EVIDENCE_PATH}{SETTLED_RUNS}/{run}/run.json")
    for run in missing:
        print(f"SETTLED names run {run}, which no record holds; nothing to retain")
    print(f"settled runs retained: {len(written)} written, {len(missing)} held by no record")
    return 1 if missing else 0


def update(*, workers: int = 1) -> int:
    expected = document(workers=workers)
    content = text(expected)
    if not RECORD.is_file() or RECORD.read_text(encoding="utf-8") != content:
        with atomic_output_file(RECORD) as temporary:
            temporary.write_text(content, encoding="utf-8")
    decisions.cache_clear()
    regularized_defaults.cache_clear()
    print(f"default drawings updated: {_summary(expected)}")
    print(f"regularization states: {_states_summary(expected['states'])}")
    return 0


def check(*, workers: int = 1) -> int:
    expected = document(workers=workers)
    found, kept = problems(expected)
    for line in kept:
        print(line)
    if found:
        for problem in found:
            print(f"default drawings drift: {problem}")
        print(f"run `{GENERATOR} --update`, or say why the rule has changed")
        return 1
    print(f"rule ({improvement_rule.SECTION}): {improvement_rule.statement()}")
    print(f"regularization states: {_states_summary(expected['states'])}")
    print(f"default drawings check passed: {_summary(expected)}")
    return 0


#: What a row of `states` says a reader sees, which `drawing_changes` compares.
SEEN = ("state", "drawn", "generator", "witness")


def _picture(row: Mapping[str, Any]) -> str:
    """A state row's drawn picture, as a line of `drawing_changes` gives it."""
    what = f"the {row['generator']} view" if row["drawn"] == VIEW else "the house drawing"
    measures = row["measures"]
    return (
        f"{row['state']}, {what} ({measures['uneven_axis']} uneven, "
        f"{measures['near_axis']} near-axis, {measures['house_total']} full shared sides)"
    )


def _side(row: Mapping[str, Any]) -> Fraction | None:
    """A state row's exact side, where its witness writes the side as a number; n = 51's
    algebraic side is not compared."""
    try:
        return Fraction(str(row["witness"]["side"]))
    except ValueError, ZeroDivisionError:
        return None


def strong_view_losses(
    earlier: Mapping[str, Any], later: Mapping[str, Any], *, house_exact: bool = False
) -> list[str]:
    """Where a strong generator's view was drawn, the goals of the improvement rule on
    which the picture drawn now is worse than it, in the policy's words, whatever drew
    the picture; else none. A strong view the axis tool's view replaces is the usual
    case after an adoption, since `--update-atlas` draws that view wherever it improves
    on the new house, which says nothing of the view the count lost: at #657, all seven
    lost strong views gave way to the axis tool's, and at n = 302 a drawing with no
    uneven and no near-axis square gave way to one with 26 and 11 (review D1 of #641).
    The measures and the side are judged as `improvement_rule` judges them. The lost view
    is exactly verified, as every view the layer draws is, so a house drawing is worse on
    exactness unless the record shows it exactly verified (`house_exact`); a side the
    record does not write as a number is not compared."""
    if earlier["drawn"] != VIEW or earlier.get("generator") not in STRONG_GENERATORS:
        return []
    _gains, worse = improvement_rule.compare(later["measures"], earlier["measures"])
    old, new = _side(earlier), _side(later)
    if old is not None and new is not None and new > old:
        worse.append(improvement_rule.SIDE)
    if later["drawn"] == HOUSE and not house_exact:
        worse.append(improvement_rule.EXACTNESS)
    return [improvement_rule.GOAL_NAMES[goal] for goal in worse]


#: Where `drawing_changes` marks a count, in the words of the runbook, the guide and
#: `adopt_houses`'s printout (review D1 of #641).
STRONG_VIEW_LOST = (
    "a strong view gives way to a drawing worse than it on a goal of the improvement "
    "rule, whatever drew it"
)
#: How `drawing_changes` names the goals a lost strong view's replacement is worse on.
LOST = "the strong view gives way to a drawing worse on"
#: How a marked line ends, which `compare` counts: a count still pending whose strong view
#: gave way to a worse drawing owes its runs in this pull request, as every count an
#: adoption re-houses does, since none is deferred. The owner, 16 October 2026: "We should
#: always be adopting the smallest packing and then regularizing it" (review E1 of #641).
RUNS_OWED = "its runs are owed in this pull request"


def drawing_changes(earlier: Mapping[str, Any], later: Mapping[str, Any]) -> list[str]:
    """Each count whose state, drawn picture or witness differs between two of these
    records, the earlier first, as one line: what each draws, in which state, with its
    uneven and near-axis squares and full shared sides, and where a strong view gives way
    to a drawing worse than it on a goal of the improvement rule, whatever drew it, those
    goals (`strong_view_losses`), and where the count still reads pending, that its runs
    are owed in this pull request (`RUNS_OWED`). A count its runs have since regularized
    or decided reads its state and is not marked (review E2 of #641). An adoption lists
    these in its pull request, from its base branch's record, so that what each re-housed
    count drew before and draws now is reviewed (reviews A1 and D1 of #641)."""
    before = {int(row["n"]): row for row in earlier.get("states") or []}
    after = {int(row["n"]): row for row in later.get("states") or []}
    exact = {
        int(entry["n"]): bool(entry["house_exact"]) for entry in later.get("entries") or []
    }
    lines: list[str] = []
    for n in sorted(before.keys() | after.keys()):
        old, new = before.get(n), after.get(n)
        if old is None or new is None:
            lines.append(f"n={n}: only in the {'later' if old is None else 'earlier'} record")
            continue
        if all(old.get(key) == new.get(key) for key in SEEN):
            continue
        rehoused = " (a new witness)" if old.get("witness") != new.get("witness") else ""
        line = f"n={n}{rehoused}: {_picture(old)} -> {_picture(new)}"
        lost = strong_view_losses(old, new, house_exact=exact.get(n, False))
        if lost:
            line += f"; {LOST} {', '.join(lost)}"
            if new["state"] == PENDING:
                line += f": {RUNS_OWED}"
        lines.append(line)
    return lines


def compare(earlier: Path, record: Path = RECORD) -> int:
    """Print `drawing_changes` from the record at `earlier` to the committed one."""
    lines = drawing_changes(
        json.loads(earlier.read_text(encoding="utf-8")),
        json.loads(record.read_text(encoding="utf-8")),
    )
    for line in lines:
        print(line)
    marked = sum(1 for line in lines if line.endswith(RUNS_OWED))
    settled = sum(1 for line in lines if f"; {LOST} " in line) - marked
    changed = f"{len(lines)} counts changed state, drawing or witness"
    print(
        f"{changed}; where {STRONG_VIEW_LOST}: {marked} still pending, whose runs are owed "
        f"in this pull request, and {settled} in another state"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="write the record")
    mode.add_argument("--check", action="store_true", help="measure again and compare")
    mode.add_argument(
        "--check-state",
        action="store_true",
        help="the regularization-state gate: the record and the index, nothing measured",
    )
    command.add_argument(
        "--base-ref",
        metavar="REF",
        help=(
            "with --check-state: hold each CORRECTED entry to the record at the merge base "
            "of REF and HEAD, which the records tier passes as origin/main"
        ),
    )
    mode.add_argument(
        "--retain-runs",
        action="store_true",
        help="copy into the evidence the index's block of each run SETTLED names that it lacks",
    )
    mode.add_argument(
        "--compare",
        type=Path,
        metavar="EARLIER",
        help=(
            "list each count whose state, drawing or witness differs from an earlier record, "
            "such as the pull request's base branch's, BASE being main unless the pull "
            f"request is stacked: `--compare <(git show origin/$BASE:{RECORD_PATH})`"
        ),
    )
    command.add_argument(
        "--workers",
        type=int,
        default=None,
        help="processes to measure with (default: the gate's PACK_JOBS cap, or every core)",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    command = parser()
    args = command.parse_args(argv)
    if args.base_ref is not None and not args.check_state:
        command.error("--base-ref goes with --check-state")
    if args.check_state:
        return check_state(args.base_ref)
    if args.retain_runs:
        return retain()
    if args.compare is not None:
        return compare(args.compare)
    workers = args.workers if args.workers is not None else worker_count(len(index_entries()))
    if args.update:
        return update(workers=workers)
    return check(workers=workers)


if __name__ == "__main__":
    raise SystemExit(main())
