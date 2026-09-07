# BC-279: Author Result and Exact Six-Core Control

**The whole seven-core target remains unresolved.** I constructed six feasible maximal
wall cores at an admitted four-square configuration and verified every required
shared-normal predicate.
This proves a lower bound of six at that configuration.
A closed covering argument also proves that a seventh core cannot be appended while
these six centers remain fixed.
It does not exclude rearrangements of the six, prove capacity at most six even at this
four-square configuration, or exclude the whole $\mathcal M_7$.

The exact six-core control and its insertion obstruction are the completed partial
results below, subject to the reserved fresh independent audit.
No seven-core witness, uniform capacity upper bound, eleven-square packing or H118
comparison is claimed.

## Unchanged Scientific Scope

This author attempt uses the complete [BC279 protocol](bc-279-wall-core-protocol.md).
The coordinator authorized dispatch after committed protocol `52b1b43e` and
runnable-record correction `d11b866f`, reporting that the immutable latter revision
passed all 31 record steps in 27.46 seconds.
Those record checks were not rerun by this author.

The target is the entire original $\Gamma_0$ at $q=96/25$, with $b=1/2$ and $d=167/50$,
all eight guards, independent actual selected angles, six complete selected SAT clauses
and every source boundary.
Seven residual centers must satisfy their exact wall graphs and all 28 cross and 21
residual pair predicates, with one common unit normal for every inequality of each pair.
The declared body is always

$$
K(r)=\operatorname{conv}\bigl(B_{1/2}\cup[-a,a]^2\bigr),\qquad
a=\frac1{4\min(r,1/\sqrt2)},\qquad
r=\min(X,Y,q-X,q-Y).
$$

No guard, normal direction, saturation branch or touching convention was changed.
The target was not replaced by disk, union or octagon capacity.
The exact construction below is a six-body control inside the declared model, not a new
target domain or a fitted center box.

## Four Actual Selected Squares

Use the exact rational selected configuration accepted in
[BC278](bc-278-boundary-band-independent-review.md), denoted $G_A$ there:

$$
e=(4/5,3/5),\qquad f=(-3/5,4/5),\qquad
\theta=\arctan(3/4).
$$

| Selected slot | Center |
| --- | --- |
| $0$ | $(7/10,7/10)$ |
| $1$ | $(1269/850,1113/850)$ |
| $2$ | $(399/170,7/10)$ |
| $3$ | $(157/50,1113/850)$ |

All four choose this same permitted angle at this one point of the independent-angle
domain.
Their coordinate support is $7/10$. The extreme horizontal wall positions and the
low row are contained with legal equality.
The high row lies below the lower band ceiling with exact margin $7/51$.

For pairs $01,12,23,02,13,03$, actual normals $e,-f,e,e,e,e$ give respective projections

$$
1,\quad1,\quad1,\quad112/85,\quad112/85,\quad197/85.
$$

Their support sums are one, so this is the complete six-pair selected SAT inventory.
The three adjacent equalities are legal contacts, not omissions from the domain.
The horizontal gaps are $337/425,363/425,337/425$.

The source guard quantities are

$$
m=5/8,\quad\varepsilon=0,\quad\ell=7/10,\quad u=1113/850,
\quad\Delta=259/425,\quad A=41/40.
$$

In the protocol’s order, the eight exact guard values are

$$
259/425,\quad991/8500,\quad733/3400,\quad99/1000,\quad99/1000,
\quad3523/8500,\quad3003/8500,\quad3523/8500.
$$

All are positive. Thus $G_A\in\Gamma_0$. This membership and the construction below do
not assert membership of any eleven-square configuration in $D_0$.

## Six Residual Centers and Their Exact Wall Graphs

Put $w=259/300$. Four upper centers alternate between heights $643/200$ and $523/200$,
with common horizontal gap $w$. Add one left and one middle lower center:

| Core | Center $W_j$ | $r_j$ | $a_j$ |
| --- | --- | --- | --- |
| $0$ | $(5/8,643/200)$ | $5/8$ | $2/5$ |
| $1$ | $(893/600,523/200)$ | $49/40$ | $\sqrt2/4$ |
| $2$ | $(1411/600,643/200)$ | $5/8$ | $2/5$ |
| $3$ | $(643/200,523/200)$ | $5/8$ | $2/5$ |
| $4$ | $(5/8,2)$ | $5/8$ | $2/5$ |
| $5$ | $(58/25,39/20)$ | $38/25$ | $\sqrt2/4$ |

Every center lies in $[1/2,167/50]^2$. Each displayed $r_j$ is the minimum of its four
actual wall distances.
In particular core 0 has an exact left/top minimum tie; both owner branches are
retained. For the four values $r=5/8$, $r^2=25/64<1/2$ and $4ar=1$. For cores 1 and 5,
$r>1/\sqrt2$ and $8a^2=1$ with $a>0$. They are exactly disks, while the other four are
the larger declared hulls.
No midpoint value or adjustable auxiliary is used.

All radicals below mean their positive real roots: $\sqrt2>0$ with square two and
$\sqrt7>0$ with square seven.
Define

$$
c_*=(5+\sqrt7)/8,\qquad s_*=(5-\sqrt7)/8.
$$

Then $c_*^2+s_*^2=1$, both are positive, and $c_*+s_*=5/4$. Set

$$
T=\frac{2195+79\sqrt7}{2400}>1.
\tag{1}
$$

For the strict inequality, $79\sqrt7>205$ follows by squaring positive quantities:
$7\cdot79^2-205^2=1662>0$.

## All 15 Residual Pair Normals

For a unit normal the exact support is $h_{K_j}(n)=\max(1/2,a_j(|n_x|+|n_y|))$. The
following normal is directed from $W_j$ to $W_k$ for each $j<k$. The column $S$ is the
sum of the two exact hull supports on that same normal.
Thus $D\ge S$ certifies all four protocol inequalities for that pair at once.

| Pair | Unit normal $n$ | $D=n\cdot(W_k-W_j)$ | $S=h_{K_j}(n)+h_{K_k}(n)$ |
| --- | --- | --- | --- |
| $01$ | $(c_*,-s_*)$ | $T$ | $1$ |
| $02$ | $(1,0)$ | $259/150$ | $1$ |
| $03$ | $(1,0)$ | $259/100$ | $1$ |
| $04$ | $(0,-1)$ | $243/200$ | $1$ |
| $05$ | $(1,0)$ | $339/200$ | $1$ |
| $12$ | $(c_*,s_*)$ | $T$ | $1$ |
| $13$ | $(1,0)$ | $259/150$ | $1$ |
| $14$ | $(-12/13,-5/13)$ | $2687/2600$ | $133/130$ |
| $15$ | $(4/5,-3/5)$ | $3193/3000$ | $1$ |
| $23$ | $(c_*,-s_*)$ | $T$ | $1$ |
| $24$ | $(-1,0)$ | $259/150$ | $1$ |
| $25$ | $(0,-1)$ | $253/200$ | $1$ |
| $34$ | $(-1,0)$ | $259/100$ | $1$ |
| $35$ | $(-4/5,-3/5)$ | $223/200$ | $53/50$ |
| $45$ | $(1,0)$ | $339/200$ | $1$ |

All normals are exactly unit.
On coordinate normals every hull has support $1/2$. For the three adjacent upper pairs,
$L=|n_x|+|n_y|=5/4$, so a core with $a=2/5$ has support $1/2$ exactly; a disk has
support $1/2$ too. Their displacement gives $c_*w+s_*(3/5)=T$, proving those three rows
with the same normal for every support term.

For pair 14, $L=17/13$. The disk has support $1/2$ and the $a=2/5$ hull has support
$34/65$, giving $S=133/130$. Its exact positive margin is $27/2600$. Pair 15 joins two
disks, so $S=1$. For pair 35, $L=7/5$, giving supports $14/25$ and $1/2$, with margin
$223/200-53/50=11/200$. Every other margin is positive directly from the table.
The inventory contains each of the 15 unordered pairs exactly once.

## All 24 Cross Normals Against the Actual Selected Squares

The following checks use the actual selected-square support $H_i$, not a disk or
axis-core replacement of a selected square.
Normals point from $C_i$ to $W_j$.

For all 16 pairs with residual index $j=0,1,2,3$, use the same explicit construction
$v_{ij}=(0,1)$. Here $H_i(v)=7/10$ and $h_{K_j}(v)=1/2$, so the required support sum is
$6/5$. The smallest directed displacement in these 16 pairs is

$$
523/200-1113/850=4439/3400>6/5,
$$

with margin $359/3400$. This verifies both shared-normal inequalities for every pair in
the group, including those whose residual body is a hull rather than a disk.

The remaining eight pairs have these exact certificates:

| Selected $i$ | Residual $j$ | Unit normal $v_{ij}$ | Directed displacement | Actual support sum |
| --- | --- | --- | --- | --- |
| $0$ | $4$ | $(0,1)$ | $13/10$ | $6/5$ |
| $1$ | $4$ | $f=(-3/5,4/5)$ | $3649/3400$ | $53/50$ |
| $2$ | $4$ | $(-1,0)$ | $1171/680$ | $6/5$ |
| $3$ | $4$ | $(-1,0)$ | $503/200$ | $6/5$ |
| $0$ | $5$ | $(0,1)$ | $5/4$ | $6/5$ |
| $1$ | $5$ | $e=(4/5,3/5)$ | $8891/8500$ | $1$ |
| $2$ | $5$ | $f=(-3/5,4/5)$ | $4319/4250$ | $1$ |
| $3$ | $5$ | $f=(-3/5,4/5)$ | $4269/4250$ | $1$ |

For $(i,j)=(1,4)$, the selected support on $f$ is $1/2$ and the hull support is
$(2/5)(7/5)=14/25$, giving $53/50$ and margin $9/680$. For the last three rows core 5 is
a disk and each selected support is $1/2$. All remaining coordinate-normal sums are
$7/10+1/2=6/5$. Thus every row uses one unit normal satisfying both cross inequalities,
with positive margin.

There are exactly $16+8=24$ cross pairs.
Together with the 15 residual rows, these are all **39 normals required for six cores**.
They are not a 49-normal certificate for seven cores.
The source, graph and separation checks prove only

$$
\kappa_{\rm wall}(G_A)\ge6.
\tag{2}
$$

## A Seventh Core Cannot Be Appended to These Fixed Six

This is a complete refusal of one construction mechanism, with its scope fixed
explicitly: keep $G_A$ and the six displayed centers, and allow the proposed seventh
center to vary everywhere permitted by the model.
Rearranging any of the existing six is outside this insertion statement.

The accepted source-guard localization in the
[BC278 audit](bc-278-boundary-band-independent-review.md) gives, at $G_A$,

$$
[b,d]\times[b,\ell+A]\subseteq\bigcup_i\mathcal O_i,
\qquad \ell+A=69/40,
$$

where $\mathcal O_i$ denotes the old selected guard octagons, distinguished from the new
residual common cores.
Even each closed $\mathcal O_i$ is strictly forbidden to the center of a disk avoiding
the four actual selected squares.
A further core contains its radius-$1/2$ disk, so its center must satisfy $Y>69/40$ and
lie in

$$
\mathcal R=[b,d]\times[69/40,d].
$$

This rectangle is a necessary consequence of the source geometry at the fixed control,
not a fitted parent box.
I now cover it strictly by the open unit-radius disks about the six existing centers.

Partition it into the following three closed horizontal strips.
In each row, the listed center supplies a horizontal interval of halfwidth $\rho$ at
every height in that strip.
The bound $|Y-W_{j,y}|\le v$ and $\rho^2+v^2<1$ puts the entire corresponding closed
rectangle strictly inside the open unit disk about $W_j$.

| Strip height interval | Centers and halfwidths $\rho$ | Corresponding vertical bounds $v$ |
| --- | --- | --- |
| $[69/40,49/20]$ | $W_4:89/100$; $W_5:43/50$; $W_3:9/20$ | $9/20$; $1/2$; $89/100$ |
| $[49/20,543/200]$ | $W_0:3/5$; $W_1:49/50$; $W_2:3/5$; $W_3:49/50$ | $153/200$; $33/200$; $153/200$; $33/200$ |
| $[543/200,167/50]$ | $W_0:173/200$; $W_2:173/200$; $W_3:17/25$ | $1/2$; $1/2$; $29/40$ |

The distinct squared-radius sums in this table are

$$
9946/10000,\quad2474/2500,\quad37809/40000,\quad
39505/40000,\quad39929/40000,\quad39521/40000,
$$

all strictly below one.
To check horizontal coverage:

- In the lowest strip, $W_4,W_5$ have center gap $339/200$ and halfwidth sum $7/4$;
  $W_5,W_3$ have gap $179/200$ and halfwidth sum $131/100$. The extreme intervals extend
  beyond both $b$ and $d$.
- In the middle strip, consecutive upper centers have gap $259/300$, while each
  neighboring halfwidth sum is $79/50$. The extremes again extend past both sides.
- In the highest strip, $W_0,W_2$ have gap $259/150$ and halfwidth sum $173/100$, with
  positive overlap $1/300$. The next gap is $259/300$ and its halfwidth sum is
  $309/200$. The extreme intervals reach beyond both sides.

Thus every point of the closed $\mathcal R$ has distance strictly less than one from at
least one $W_j$. The strip seams are included in both neighboring strips; none is lost
to a strict endpoint convention.
Every possible added core would therefore overlap the incircle of an existing core in
their interiors. No unit normal could satisfy its pair predicate with that core.

The exact conclusion is **insertion maximality of this fixed six-core packing**. It does
not prove $\kappa_{\rm wall}(G_A)\le6$: a different arrangement of six or seven centers
is not constrained by these exclusion disks.
In particular, open unit-radius coverage is not a partition into regions of capacity
one. Treating it as such would be a false capacity argument.

## What Remains Unproved

The construction work explored an upper zigzag group with lower cavity occupants.
The displayed exact six-core arrangement is the completed feasible result of that
attempt. The covering argument closes adding a seventh while holding it fixed.
No claim is made for other unverified coordinate choices, a moving six-core family, or
an arbitrary member of $\Gamma_0$.

The old seven-disk witness is still rejected by the protocol’s wall-core control; its
failure does not constrain all other seven-center configurations.
The six-core control shows that a proposed uniform bound below six would be false, and
would be a useful feasible control for any later claimed bound of six.
It is not evidence that the bound of six is true.

The exact missing implication remains whether every seven variable centers over every
$G\in\Gamma_0$ fail at least one of the 49 complete common-normal predicates.
No complete treatment of those moving centers, changing nearest-wall branches, selected
actual angles and mutual pair normals was obtained.
The admitted model already incorporates the maximal individual wall-conditioned core;
this partial result does not license replacing it by a weaker core or adding a new
premise.

All results above transfer by joint affine reflection of the four selected centers and
six residual centers, and linear reflection of every normal and displacement.
The actual selected angles change sign.
Wall graphs and core supports are preserved.
The fixed-insertion statement reflects with the entire configuration and its necessary
center region. The full three-band cover, angle endpoints, counting seam convention,
every label/order parent and every failure sibling remain unchanged.
No full-square parent child is pruned by this partial result.

No exact seven-core witness, full-square eleven-pose witness or surviving point of a
matched coupled LP was produced.
Hence the whole $\mathcal M_7$, full-square $D_0$ and strict H118 comparison all retain
their unresolved status.
The next action is the reserved fresh independent audit of the two terminal reports.
This author report does not authorize a target continuation, a different model or an
engine.

## Work Receipt

The prospective author lease was 11:36:33–12:06:33 UTC on 2026-09-07. The actual first
clock read after dispatch was **11:38:50 UTC**. I read the immutable native protocol and
used the previously accepted exact source configuration and localization.
I did not read the active adversary report or exchange target reasoning with the
adversary or the reserved fresh auditor.
Only the coordinator received interim findings.

All scientific work was hand analysis and exact construction.
No numerical target, script, solver, engine, resource search, fitted pose box,
weaker-model retry, Git mutation, shared-record edit, new identifier or dependency
change occurred. Only this assigned native report was written.
The mathematical argument and full exact readback froze at **12:01:02 UTC**, an elapsed
**22 minutes 12 seconds** from the actual first clock read.
The 15 residual normals, 24 cross normals, source guards, wall graphs and three-strip
insertion cover were checked by hand.
The common-document and prose-editing passes were applied.
Installed Flowmark 0.4.0 formatted this file and passed its no-cache check; both linked
source files exist, the footer appears once, and the trailing-whitespace scan found no
matches. A final scoped formatting check follows this receipt before terminal handoff,
within the original **12:06:33 UTC** hard stop.
No mathematical work resumes after this freeze.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
