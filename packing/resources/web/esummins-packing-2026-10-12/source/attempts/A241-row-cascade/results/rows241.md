# A241 -- the ROW cascade: the one-slot extensions of the protected tier and A55's k4 kills

A class gets a **full-window row** `FULL [191/50, 969271/250000]` when, and only when, one of two things holds
(`code/rowcascade241.py` docstring carries the contract):

* **(A) a direct window certificate** -- a `parametric-kill-certificate-v1` 4D PASS over the window plus
  canary C2 at 191/50 / midpoint / s0.  `closed_disjoint_bridge.md` B.2 then instantiates `stratum_kill`
  at every m in the window.
* **(B) the Lemma K1(i) climb** -- `instratum_bridge.md` E.1(i): a class CONTAINING an already-rowed class
  inherits its row (slots_S(s) is a D4 image of a subset of slots_S'(s) at every side s).

**What is NOT a row, and the correction A241 has to make to its own brief.**  "Row C when every one-slot
EXTENSION of C is full-window closed" is unsound: K1 climbs UP containment, and a packing whose skeleton is
exactly C has no fifth simple square, so C's extensions never apply to it.  Closed extensions give Lemma
SLOT-CROWD (`slot_crowds.md` s.2) -- every such slot of C is met by >= 2 non-pin squares -- i.e. C's
FORCED CELLS, the toolkit's traction (A238), not C's emptiness.  Promoting "all slots doubly met" to
"C is empty" is the crowd certificate CS(S; ...) of `slot_crowds.md` s.4, and A94 measured that it does
NOT certify (runs B2-B4 FAIL, 30-32 exact holes).  So the CASCADE below is (A) + (B), and what it hands
the k <= 3 tier is forced cells, which is exactly the lever A238 asked for.

**Why A55's eight exact k4 kills were not already rows.**  They are certified AT s0.
`closed_disjoint_bridge.md` B.2: the corpus containment margin is rho ~ 1.0000009e-9 with A = 5/2, so
(H') reads s''/m - 1 < 4.0e-10 -- an s0-anchored PASS instantiates the kill at NO side of [3.82, s-hat]
whatsoever.  The window statement is therefore real work: A56's parametric layer, re-run on A55's base
certificates.  That campaign is `code/param241.py` (resumable, `code/param241.sh`).

## 1. The window-statement campaign (source (A)) -- A55's exact k <= 4 kills

| class | base certificate | atoms | stage 0 at 191/50 (gap / nearest-wall / mid-band) | 4D over the window | C2 | ROW |
|---|---|---|---|---|---|---|
| `k4_07` | attempts\A55-k4-sweep\certs\k4_07.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 134.7s / nearest-wall rc=1 161.3s / mid-band rc=1 132.1s | - | PARAM-FAIL |
| `k4_10` | attempts\A55-k4-sweep\certs\k4_10.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 353.5s / nearest-wall rc=1 1687.9s / mid-band rc=1 310.9s | - | PARAM-FAIL |
| `k4_12` | attempts\A55-k4-sweep\certs\k4_12.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 653.6s / nearest-wall rc=124 2400.0s / mid-band rc=1 399.6s | - | PARAM-FAIL |
| `k4_02` | attempts\A55-k4-sweep\certs\k4_02.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 625.7s / nearest-wall rc=124 2400.0s / mid-band rc=1 520.6s | - | PARAM-FAIL |
| `k4_04` | attempts\A55-k4-sweep\certs\k4_04.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 363.1s / nearest-wall rc=1 530.7s / mid-band rc=1 330.4s | - | PARAM-FAIL |
| `k4_00` | attempts\A55-k4-sweep\certs\k4_00.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 752.5s / nearest-wall rc=1 2008.2s / mid-band rc=1 526.6s | - | PARAM-FAIL |
| `k4_01` | attempts\A55-k4-sweep\certs\k4_01.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 1053.3s / nearest-wall rc=124 2400.1s / mid-band rc=1 1013.1s | - | PARAM-FAIL |
| `k4_09` | attempts\A55-k4-sweep\certs\k4_09.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=124 2400.1s / nearest-wall rc=124 2400.0s / mid-band rc=1 839.0s | - | PARAM-FAIL |
| `k3_00` | attempts\A55-k4-sweep\k3_ext\certs\k3_00.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 1180.9s / nearest-wall rc=124 2400.0s / mid-band rc=1 856.6s | - | PARAM-FAIL |
| `k4_07` | attempts\A55-k4-sweep\certs\k4_07.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 154.0s / nearest-wall rc=1 193.7s / mid-band rc=1 168.0s | - | PARAM-FAIL |
| `k4_10` | attempts\A55-k4-sweep\certs\k4_10.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 475.5s / nearest-wall rc=1 2287.2s / mid-band rc=1 428.2s | - | PARAM-FAIL |
| `k4_12` | attempts\A55-k4-sweep\certs\k4_12.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 890.4s / nearest-wall rc=1 2934.8s / mid-band rc=1 618.1s | - | PARAM-FAIL |
| `k4_02` | attempts\A55-k4-sweep\certs\k4_02.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 969.4s / nearest-wall rc=124 5400.1s / mid-band rc=1 598.0s | - | PARAM-FAIL |
| `k4_04` | attempts\A55-k4-sweep\certs\k4_04.json | - | gap PASS / nearest-wall PASS / mid-band PASS | gap rc=1 432.8s / nearest-wall rc=1 646.3s / mid-band rc=1 401.4s | - | PARAM-FAIL |

## 2. The extension table

| class | own row | forced cells | USABLE | extension -> status |
|---|---|---|---|---|
| `trump5` | -- | 6 | **6** | BL(0,2)→k6_07 [FULL-WINDOW], BL(1,1)→k6_19 [FULL-WINDOW], BR(0,1)→k6_21 [FULL-WINDOW], TR(0,1)→k6_22 [FULL-WINDOW], TR(1,0)→k6_24 [FULL-WINDOW], TL(0,0)→k6_23 [FULL-WINDOW] |
| `k4_03` | -- | 5 | **3** | BL(1,1)→k5_09 [FULL-WINDOW], BL(2,0)→k5_02 [FULL-WINDOW], BR(0,0)→k5_11 [OPEN], TR(0,0)→trump5 [OPEN], TL(1,0)→k5_10 [FULL-WINDOW] |
| `k4_05` | -- | 5 | **3** | BL(1,0)→k5_11 [OPEN], BR(0,1)→k5_15 [FULL-WINDOW], BR(1,0)→k5_13 [FULL-WINDOW], TR(0,0)→k5_16 [OPEN], TL(1,0)→k5_12 [FULL-WINDOW] |
| `k4_06` | -- | 5 | **3** | BL(1,0)→trump5 [OPEN], BR(0,0)→k5_16 [OPEN], TR(0,1)→k5_17 [FULL-WINDOW], TR(1,0)→k5_14 [FULL-WINDOW], TL(1,0)→k5_13 [FULL-WINDOW] |
| `k4_08` | -- | 7 | **5** | BL(0,2)→k5_03 [FULL-WINDOW], BL(1,1)→k5_18 [FULL-WINDOW], BL(2,0)→k5_03 [FULL-WINDOW], BR(0,0)→trump5 [OPEN], TR(0,1)→k5_19 [FULL-WINDOW], TR(1,0)→k5_19 [FULL-WINDOW], TL(0,0)→trump5 [OPEN] |
| `k4_11` | -- | 7 | **5** | BL(0,2)→k5_07 [FULL-WINDOW], BL(1,0)→trump5 [OPEN], BR(0,1)→k5_15 [FULL-WINDOW], BR(1,0)→k5_12 [FULL-WINDOW], TR(0,1)→k5_17 [FULL-WINDOW], TR(1,0)→k5_20 [FULL-WINDOW], TL(0,0)→k5_16 [OPEN] |
| `corners4` | -- | 8 | **0** | BL(0,1)→k5_16 [OPEN], BL(1,0)→k5_16 [OPEN], BR(0,1)→k5_16 [OPEN], BR(1,0)→k5_16 [OPEN], TR(0,1)→k5_16 [OPEN], TR(1,0)→k5_16 [OPEN], TL(0,1)→k5_16 [OPEN], TL(1,0)→k5_16 [OPEN] |
| `k3_01` | -- | 4 | **0** | BL(1,0)→k4_03 [OPEN], BR(0,0)→k4_05 [OPEN], TR(0,0)→k4_06 [OPEN], TL(1,0)→k4_04 [s0 only] |
| `k3_02` | -- | 6 | **0** | BL(0,2)→k4_00 [s0 only], BL(1,1)→k4_07 [s0 only], BL(2,0)→k4_00 [s0 only], BR(0,0)→k4_03 [OPEN], TR(0,0)→k4_08 [OPEN], TL(0,0)→k4_03 [OPEN] |
| `k3_03` | -- | 6 | **0** | BL(0,2)→k4_01 [s0 only], BL(1,0)→k4_03 [OPEN], BR(0,1)→k4_10 [s0 only], BR(1,0)→k4_04 [s0 only], TR(0,0)→k4_11 [OPEN], TL(0,0)→k4_05 [OPEN] |
| `k3_04` | -- | 6 | **0** | BL(0,2)→k4_02 [s0 only], BL(1,0)→k4_08 [OPEN], BR(0,0)→k4_11 [OPEN], TR(0,1)→k4_12 [s0 only], TR(1,0)→k4_09 [s0 only], TL(0,0)→k4_06 [OPEN] |
| `k3_05` | -- | 7 | **0** | BL(0,1)→k4_05 [OPEN], BL(1,0)→k4_05 [OPEN], BR(0,1)→k4_11 [OPEN], BR(1,0)→k4_06 [OPEN], TR(0,0)→k4_13 [OPEN], TL(0,1)→k4_06 [OPEN], TL(1,0)→k4_11 [OPEN] |
| `k2_00` | -- | 5 | **0** | BL(0,2)→k3_00 [no row], BL(1,0)→k3_02 [OPEN], BR(0,0)→k3_03 [OPEN], TR(0,0)→k3_04 [OPEN], TL(0,0)→k3_01 [OPEN] |
| `k2_01` | -- | 6 | **0** | BL(0,1)→k3_01 [OPEN], BL(1,0)→k3_03 [OPEN], BR(0,0)→k3_05 [OPEN], TR(0,0)→k3_05 [OPEN], TL(0,1)→k3_01 [OPEN], TL(1,0)→k3_03 [OPEN] |
| `k2_02` | -- | 6 | **0** | BL(0,1)→k3_04 [OPEN], BL(1,0)→k3_04 [OPEN], BR(0,0)→k3_05 [OPEN], TR(0,1)→k3_04 [OPEN], TR(1,0)→k3_04 [OPEN], TL(0,0)→k3_05 [OPEN] |
| `k1_00` | -- | 5 | **0** | BL(0,1)→k2_00 [OPEN], BL(1,0)→k2_00 [OPEN], BR(0,0)→k2_01 [OPEN], TR(0,0)→k2_02 [OPEN], TL(0,0)→k2_01 [OPEN] |
| `k4_00` | -- | 4 | **4** | BL(1,1)→k5_00 [FULL-WINDOW], BL(2,0)→k5_01 [FULL-WINDOW], BR(0,0)→k5_02 [FULL-WINDOW], TR(0,0)→k5_03 [FULL-WINDOW] |
| `k4_01` | -- | 4 | **4** | BL(1,0)→k5_02 [FULL-WINDOW], BR(0,1)→k5_06 [FULL-WINDOW], BR(1,0)→k5_04 [FULL-WINDOW], TR(0,0)→k5_07 [FULL-WINDOW] |
| `k4_02` | -- | 4 | **4** | BL(1,0)→k5_03 [FULL-WINDOW], BR(0,0)→k5_07 [FULL-WINDOW], TR(0,1)→k5_08 [FULL-WINDOW], TR(1,0)→k5_05 [FULL-WINDOW] |
| `k4_04` | -- | 4 | **4** | BL(1,0)→k5_10 [FULL-WINDOW], BR(0,0)→k5_12 [FULL-WINDOW], TR(0,0)→k5_13 [FULL-WINDOW], TL(2,0)→k5_04 [FULL-WINDOW] |
| `k4_07` | -- | 5 | **5** | BL(0,2)→k5_00 [FULL-WINDOW], BL(2,0)→k5_00 [FULL-WINDOW], BR(0,0)→k5_09 [FULL-WINDOW], TR(0,0)→k5_18 [FULL-WINDOW], TL(0,0)→k5_09 [FULL-WINDOW] |
| `k4_09` | -- | 6 | **6** | BL(0,2)→k5_05 [FULL-WINDOW], BL(1,0)→k5_19 [FULL-WINDOW], BR(0,0)→k5_20 [FULL-WINDOW], TR(0,1)→k5_19 [FULL-WINDOW], TR(2,0)→k5_05 [FULL-WINDOW], TL(0,0)→k5_14 [FULL-WINDOW] |
| `k4_10` | -- | 6 | **6** | BL(0,2)→k5_06 [FULL-WINDOW], BL(1,0)→k5_10 [FULL-WINDOW], BR(0,2)→k5_06 [FULL-WINDOW], BR(1,0)→k5_10 [FULL-WINDOW], TR(0,0)→k5_15 [FULL-WINDOW], TL(0,0)→k5_15 [FULL-WINDOW] |
| `k4_12` | -- | 6 | **6** | BL(0,2)→k5_08 [FULL-WINDOW], BL(1,0)→k5_19 [FULL-WINDOW], BR(0,0)→k5_17 [FULL-WINDOW], TR(0,2)→k5_08 [FULL-WINDOW], TR(1,0)→k5_19 [FULL-WINDOW], TL(0,0)→k5_17 [FULL-WINDOW] |
| `k3_00` | -- | 3 | **0** | BL(1,0)→k4_00 [s0 only], BR(0,0)→k4_01 [s0 only], TR(0,0)→k4_02 [s0 only] |

## 3. Who can be rowed TODAY, and who waits on what

* **TODAY, and on nothing but CPU:** `k3_00` and the eight A55-killed k4 classes
  (`k4_00`, `k4_01`, `k4_02`, `k4_04`, `k4_07`, `k4_09`, `k4_10`, `k4_12`).  Each already has its
  own A55 `case-measure-certificate-v1` PASS; the only missing step is the parametric re-expression
  and the 4D run of section 1.  `k4_00` / `k4_01` / `k4_02` have a second route: each CONTAINS
  `k3_00` (D4 `id`, A55 `cap.json` witness), so once `k3_00` rows they row by (B) for free.
* **NEVER by certificate:** the six protected k4 classes `k4_03`, `k4_05`, `k4_06`, `k4_08`,
  `k4_11`, `k4_13`=`corners4` and the ten open k <= 3 classes.  Lemma K1(ii) (`instratum_bridge.md`
  E.1(ii)) forbids it: each is <= an open k5 class, so tau*(S) >= 11 - |S| and no certificate of this
  kind can exist.  Their rows can only come from the P-TREE obligation O1 per class, i.e. AFTER the
  k5 frontier closes -- they are not a bookkeeping item.
* **Waiting on the frontier (for forced cells, not for rows):** the cells of the protected k4 tier
  that extend into `trump5`, `k5_11`, `k5_16`.  Alive frontier nodes still covering each
  (A57 `PAUSED.md` census, 1590 distinct alive nodes): `k5_11` 713, `k5_16` 552, `trump5` 325.
  `corners4` is the extreme case: all eight of its cells extend into `k5_16`, so it has 0 usable
  forced cells until `k5_16` is closed on the whole window (A193 and A84 s.7.1 independently).

