<!--
Contract for this file. Prose, headings, lists, math and footnotes are Markdown, rendered
once by kpress (markdown-it: dollarmath, footnotes). Everything Markdown has no syntax for
is plain HTML, and only plain HTML: a block is a `<div class="…">` with a blank line after
the opening tag and before the closing one, so the Markdown inside still renders; an
inline run is a `<span class="…">`; figures are `<figure>` and `<figcaption>`, which kpress
decorates with its own classes. Class names are kpress's where it styles the block (hero,
subtitle, boxed-text) and the page's own only where it has none (deck, credits,
conditions). No attribute sugar (`{.class}`), no `:::` containers. Figures and the credits
carry canvas, SVG, controls and layout Markdown cannot express.
Math in Markdown text is `$…$` and `$$…$$`; math inside a raw HTML block is not seen by
Markdown, so there it stays `<span class="tex">…</span>` for the page to typeset itself.
`{{PLACEHOLDERS}}` are substituted before rendering. Each FIGURE block is stamped once
per certificate; the prose is filled once, with the headline certificate's values.
-->

<div class="doc-links screen-only">
  <a class="chip" href="{{SOURCE_URL}}" title="The Markdown this page is rendered from">MD</a>
  <a class="chip" href="t-018-explainer.pdf" title="The typeset PDF of this page">PDF</a>
  <a class="chip" href="{{REPO_URL}}" title="The project on GitHub"><svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>GITHUB</a>
</div>

<div class="hero">

# <span class="tex">s({{N}})</span> ≥ {{CURRENT_BOUND_DEC}}

<p class="subtitle centred">{{SUBTITLE}}</p>

<div class="credits centred">
  <span>Human oversight: <a href="https://x.com/ojoshe"><strong>Joshua Levy</strong></a></span>
  <span>Agents: <strong>Opus 5</strong>, <strong>Fable 5.1</strong>, and <strong>Codex 5.6</strong></span>
  <span><a href="https://github.com/jlevy/squares"><strong>github.com/jlevy/squares</strong></a></span>
  <span class="publication-date">{{PUBLISHED}} ({{EDITION}})</span>
</div>

</div>

## The Current Bound for Packing 11 Squares

The current certified bracket for this long-standing open geometry problem is
${{CURRENT_BOUND_INLINE_TEX}} \le s(11) \le {{BEST_PACKING_LONG_TEX}}$.

The lower end is the weak limit ${{CURRENT_BOUND_DEC}}$ from T-026. “Weak” matters: the
proof rules out every smaller container but does not decide whether eleven unit squares
fit at that exact endpoint.
T-026 supplies exact certificates at rational sides arbitrarily close to that limit,
including sides above $3.82$. The largest side named by a separately retained endpoint
certificate is $191/50 = 3.82$, established first by T-025.

This appears to be the first improvement in {{YEARS_SINCE_PRIOR}} years on the smallest
open case of the square packing problem.[^novelty] Stromquist published the previous
bound of {{PRIOR_LOWER_DEC}} in {{PRIOR_YEAR}}.[^stromquist-history][^repair] The
tightest known packing, due to Trump in 1979 (Figure 1), shows
<span class="math-reference">$s(11) \le {{BEST_PACKING_TEX}}$.[^trump]</span>

<figure>
  <div class="stage trump"><a href="{{BEST_RENDER_URL}}" aria-label="The rendering in the repository">{{TRUMP_SVG}}</a></div>
  <figcaption><strong>Figure 1.</strong> Eleven unit squares inside a square of side
  <span class="tex">{{BEST_PACKING_TEX}}</span>, a root of an eighth-degree polynomial.</figcaption>
</figure>

The visual lesson below starts with T-018, a simpler point-only certificate at
$381/100 = 3.81$. It places {{HEADLINE_N_ATOMS}} rationally weighted points in the
container and selects a net of {{HEADLINE_N_DIRECTIONS}} rationally parameterized
directions. Five exact conditions and a counting argument prove that endpoint before the
final section adds the threshold atoms used by T-025 and T-026.<!--BEGIN:CLAIM-->
[Verification](#verifiable-claim) of the point certificate uses exact rational
arithmetic: the one-file checker,
{{PINNED_VERIFIER_LINES}}
of standard-library Python and short enough to read in one sitting, decides the
certificate file of {{HEADLINE_N_ATOMS}} weighted points in
{{HEADLINE_PINNED_RUNTIME}}.<!--END:CLAIM-->

## The Agentic Research Framework

<div class="boxed-text">

*All of this project’s documents and code, including this paper, are written by agents.
The repository uses a flexible but defined **agentic research framework**, which is
fully documented in [the repository](https://github.com/jlevy/squares).*

</div>

This lower bound is one of {{N_RESULTS}} results the framework has registered so far,
{{N_NOVEL}} of them apparently new.
These include improved lower bounds for $n = 12$, $17$, and $19$.[^other-results] The
atlas of best known packings for every $n$ from 1 to 100 in Figure 2 comes from the same
research agenda and currently includes {{N_STARRED}} new lower bounds.

The repository includes:

- A comprehensive survey of previous research
- The atlas of packings
- A hypothesis registry
- An experiment ledger
- Exact verifiers and other tools
- A retention gate that labels results according to epistemic status (levels of
  verification, confirmation, significance, and novelty)

Work is planned on a regular cadence, typically in blocks of 8 to 12 hours, with
strategic human input on priorities and insights.
Agents then break the work into defined workflows, including research survey,
correctness verification, research loop, and optimization loop.

The framework relies on several agent tools for better engineering and workflows,
notably **[tbd](https://github.com/jlevy/tbd)** for task tracking,
**[Softschema](https://github.com/jlevy/softschema)** for structuring results, and
**[Practical Prose](https://github.com/jlevy/practical-prose)** to improve writing
quality.

Even with the best agents, research requires strategic human input.
The framework lets that input focus on strategy, while agents build on accumulated
results and tools in a research flywheel.
This approach is likely to be useful for other creative mathematical or technical
problems.

## The Square Packing Problem

The **square packing problem** asks, for each $n$, for the side $s(n)$ of the smallest
square that holds $n$ unit squares, which are free to rotate and must have disjoint
interiors.[^survey] The value of $s(n)$ is known for $n \le 10$. Stromquist proved
$s(10) = 3 + 1/\sqrt{2}$.[^stromquist-memos] The case $n = 11$ is the smallest still
open.

For values of $n$ where $s(n)$ is still unknown, results generally take the form of
upper or lower bounds.
An **upper bound** is constructive: an arrangement of $n$ unit squares in a square of
side $L$ shows that $s(n) \le L$. Trump’s packing for $n = 11$ in Figure 1 is one
example. Such constructions may be specified with approximate numerical coordinates or
derived exactly by solving the geometric relationships between touching squares.
Approximate coordinates alone do not constitute a formal proof of the upper bound.

A **lower bound** proves that $s(n) \ge L$ by ruling out every arrangement in a
container of side less than $L$. This requires an argument covering all possible
placements and rotations of the squares.
Such arguments range from simple area comparisons to detailed geometric proofs and
computer-assisted certificates.
The proof presented here is of this kind.

<figure>
  <div class="stage"><a href="known-best-1-100.pdf"><img src="known-best-1-100.svg" alt="{{COMPOSITE_ALT}}" width="2400" height="2896"></a></div>
  <figcaption><strong>Figure 2.</strong> The best known packings of 1 through 100 unit squares, with upper bounds
  and, for unsettled cases, lower bounds verified here. A crimson star marks a lower bound this project
  proved: {{N_STARRED}} of the hundred. The <a href="{{ATLAS_URL}}">repository</a> records every witness and its
  provenance. PDFs are available for <a href="known-best-1-100.pdf">this figure</a> and the
  <a href="known-best-1-324.pdf">full 324-case poster</a>.</figcaption>
</figure>

For eleven squares, the current result is $s(11) \ge {{CURRENT_BOUND_DEC}}$. We first
prove the point-only rung $s(11) \ge {{HEADLINE_L_FRAC}} =
{{HEADLINE_L_DEC}}$ because its geometry can be drawn and checked directly.
The advanced section then explains how threshold charge and dilation reach the current
bound.

<!--BEGIN:COMPARISON-->

(Some figures also show the simpler certificate for the weaker bound
$s({{N}}) \ge {{DEFAULT_L_FRAC}}$, whose smaller numbers make the argument easier to
illustrate.<!--BEGIN:REFINEMENT--> There is a small exact refinement in
[T-022]({{REFINEMENT_URL}}).<!--END:REFINEMENT-->)

<!--END:COMPARISON-->

<!--BEGIN:NO_COMPARISON-->

The figures below illustrate this certificate.

<!--END:NO_COMPARISON-->

<figure>
  <div class="line-fig kpress-diagram">
  <svg viewBox="0 0 700 260" role="img" aria-label="Number line from 3.75 to 3.90 showing the previous lower bound {{PRIOR_LOWER_DEC}}, the point and threshold bounds proved here up to {{CURRENT_BOUND_DEC}}, and the best known packing at {{BEST_PACKING_DEC}}">
    <rect x="{{BAND_X}}" y="69.5" width="{{BAND_W}}" height="13" fill="var(--cert-accent-wash)"/>
    <line x1="20" y1="76" x2="680" y2="76" stroke="var(--kpress-doc-muted)" stroke-width="1"/>
    <g stroke="var(--kpress-doc-muted)" stroke-width="1">
      <line x1="20" y1="71.5" x2="20" y2="80.5"/><line x1="460" y1="71.5" x2="460" y2="80.5"/>
      <line x1="680" y1="71.5" x2="680" y2="80.5"/>
    </g>
    <g fill="var(--kpress-doc-muted)" text-anchor="middle">
      <text x="20" y="100" text-anchor="start">3.75</text><text x="460" y="100">3.85</text><text x="680" y="100" text-anchor="end">3.90</text>
    </g>
    <line x1="{{PRIOR_X}}" y1="56" x2="{{PRIOR_X}}" y2="76" stroke="var(--kpress-doc-muted)" stroke-width="1.25"/>
    <circle cx="{{PRIOR_X}}" cy="76" r="3.2" fill="var(--kpress-doc-muted)"/>
    <g text-anchor="middle">
      <text x="{{PRIOR_X}}" y="52" fill="var(--kpress-doc-text)">{{PRIOR_LOWER_DEC}}</text>
      <text x="{{PRIOR_X}}" y="20" fill="var(--kpress-doc-muted)">{{PRIOR_SOURCE}}</text>
      <text x="{{BEST_X}}" y="52" fill="var(--kpress-doc-text)">{{BEST_PACKING_DEC}}</text>
      <text x="{{BEST_X}}" y="20" fill="var(--kpress-doc-muted)">{{BEST_SOURCE}}</text>
    </g>
    <line x1="{{BEST_X}}" y1="56" x2="{{BEST_X}}" y2="76" stroke="var(--kpress-doc-muted)" stroke-width="1.25"/>
    <circle cx="{{BEST_X}}" cy="76" r="3.2" fill="var(--kpress-doc-muted)"/>
    {{NUMBER_LINE_MARKS}}
  </svg>
  </div>
  <figcaption><strong>Figure 3.</strong> Bounds on <span class="tex">s(11)</span>. The shaded band is the gap left by the certificates explained here. At the current weak lower bound the gap is
  <span class="tex">{{CURRENT_GAP}}</span> wide, down from <span class="tex">{{GAP_BEFORE}}</span> at Stromquist’s bound.</figcaption>
</figure>

## The Five Conditions for a Point Certificate

We prove $s(11) \ge {{HEADLINE_L_FRAC}} = {{HEADLINE_L_DEC}}$ with a new weighted-point
certificate found by our automated search.
The five conditions below follow the finite certificate method used by Burns and
Massaccesi.[^burns][^massaccesi][^lineage]

The proof uses a finite **certificate**: for $n$ unit squares in a container of side
$L$, a finite set of points in the container, each with a nonnegative rational weight
(the atoms; every weight in this certificate is positive), a net of directions
$\theta_k = 2\arctan t_k$ with rational half-tangents
$0 = t_0 \lt t_1 \lt \cdots \lt t_K$, and a shrink $B$, such that:

<div class="conditions boxed-text">

**Condition 1.** The atom positions and weights are invariant under the container’s
symmetry group $\mathbf{D}_4$, its four rotations and four reflections.

**Condition 2.** The total mass of the atoms, the sum of all their weights, is strictly
below $n$.

**Condition 3.** The net reaches $\pi/4$: its last half-tangent is at least
$\tan(\pi/8)$.

**Condition 4.** $B(1 + D) \lt 1$, where $D$ is the largest of the net’s half-gap
tangents, each the tangent of half the angle between two consecutive net directions.

**Condition 5.** At every net direction, every placement of a closed square of side $B$
inside the container covers mass at least $1$.

</div>

Conditions 1 to 4 are exact rational comparisons.
Condition 5 is one exact sweep per direction.
Together the five prove $s(n) \ge L$. The certificate is [`{{ID}}`]({{CERT_URL}}) (a
weaker but simpler one is at [`{{DEFAULT_ID}}`]({{DEFAULT_CERT_URL}})). Every figure
below is [computed]({{RENDERER_URL}}) from the certificate it shows.

## Atoms, Mass, and the Budget

An **atom** is a point in the container with a nonnegative rational weight, and here
every weight is positive.
The **mass** $\mu(R)$ of a region is the sum of the weights of the atoms in it, a finite
exact sum.

Suppose eleven unit squares fit in the side-{{L_DEC}} container, and suppose the atoms
have been chosen so that both of these hold:

- Every unit square that can be placed in the container holds mass at least $1$ in its
  interior.
- The total mass of all {{N_ATOMS}} atoms is below ${{N}}$.

The second is a single sum:

$$
\sum_a w_a \;=\; {{TOTAL_TEX}} \;=\; {{TOTAL_DEC}} \;\lt\; {{N}}
$$

Two packed squares may share an edge, and an atom on it lies in both.
Their interiors are disjoint, so no atom lies in two of them, and together the eleven
interiors hold mass at least ${{N}}$. The container holds only ${{TOTAL_DEC}}$. So
eleven unit squares do not fit.

Both conditions are properties of the atoms, not of any packing.
The rest of the proof makes the first one finite to check.

## The Atom Set

There are {{N_ATOMS}} atoms in {{N_ORBITS}} orbits of $\mathbf{D}_4$, the eight
rotations and reflections of the container, with {{N_WEIGHTS}} distinct weights between
${{WEIGHT_MIN}}$ and ${{WEIGHT_MAX}}$. An orbit is an atom with its images under all
eight, so the set is invariant under the group: Condition 1. That invariance is what
lets the proof check angles only up to $\pi/4$, since a square at any other angle
reflects onto that arc and covers the same mass.

<!--BEGIN:FIGURE-->

<figure class="apparatus" data-figure="4">
  <div class="split">
    <div class="stage"><canvas id="field-{{SLUG}}" width="1040" height="1040"></canvas></div>
    <div class="panel">
      <div class="readout">
        <span class="caps">Atom</span>
        <div class="tip-panel" id="field-tip-{{SLUG}}">Hover or tap an atom for its position and weight.</div>
      </div>
    </div>
  </div>
  <div class="mass-line">
    <div>Total mass in the container<span class="v tex">\mu\!\left([0,L]^2\right) = {{TOTAL_PLAIN}} = {{TOTAL_DEC}}</span></div>
    <div>Mass eleven packed unit squares would need<span class="v tex">{{N}}</span></div>
    <div>Shortfall<span class="v tex">{{SHORTFALL}}</span></div>
  </div>
  <div class="fig-choose">{{CERT_TOGGLE}}</div>
  <figcaption><strong>Figure 4.</strong> Conditions 1 and 2. The atoms. Disc area is proportional to weight. Mass gathers along the edges and in a ring inside the
  corners, where a square has least room to move, and thins in the middle. The weights are a rationalized
  solution, on these sites, of the linear program described under Generator and Verifier. The container holds less
  mass than eleven unit squares with disjoint interiors would need. Condition 2 is that comparison.</figcaption>
</figure>

<!--END:FIGURE-->

## Every Placement Covers Mass at Least One

The covering requirement on the atoms, that every placement of a unit square holds mass
at least $1$ in its interior, has three continuous parameters, two of position and one
of angle.

The proof makes it finite twice over.
The angle is snapped to a net of {{N_DIRECTIONS}}
rational directions, and the square checked at each is a slightly smaller one, of side
$B$. The next section shows why it stands in for a unit square at any angle.
Within a direction, the set of atoms under the square changes only when an atom crosses
an edge, so the positions collapse to finitely many **event cells**, on each of which
the covered mass is constant.
Condition 5 says every event cell the square’s center can reach without leaving the
container, at every net direction, carries mass at least $1$.

Figure 5 evaluates it.
Every weight is a whole multiple of ${{SCALE}}$, so the readout counts units and rounds
nothing. The least covered mass over every placement and all {{N_DIRECTIONS}}
directions is attained at direction $0$, by the square $Q$ centered at
$({{WITNESS_X_JS}}, {{WITNESS_Y_JS}})$:

$$
\mu(Q) \;=\; {{LEAST_TEX}} \;=\; {{LEAST_DEC}},
$$

a margin of {{LEAST_MARGIN}} of those units above the threshold.

<!--BEGIN:FIGURE-->

<figure class="apparatus prover" data-figure="5">
  <div class="split">
    <div class="stage"><canvas class="draggable" id="prove-{{SLUG}}" width="1000" height="1000" aria-label="Movable square and covered-mass shading" aria-describedby="hint-{{SLUG}}"></canvas></div>
    <div class="panel">
      <div class="readout">
        <span class="caps">Mass covered</span>
        <div class="mass-row">
          <div class="mass-val" id="mv-{{SLUG}}"></div>
          <div class="mass-dec" id="md-{{SLUG}}"></div>
        </div>
        <span class="verdict" id="vd-{{SLUG}}" hidden></span>
      </div>
      <div class="ctl">
        <label class="caps" for="kslider-{{SLUG}}">Choose a net direction (0–{{N_DIRECTIONS_MAX}})</label>
        <input type="range" id="kslider-{{SLUG}}" min="0" max="{{N_DIRECTIONS_MAX}}" value="0" step="1">
        <div class="val direction-values" id="kval-{{SLUG}}"></div>
      </div>
      <div class="btns">
        <button id="btn-tight-{{SLUG}}" aria-describedby="actions-{{SLUG}}">Show net minimum</button>
        <button id="btn-scan-{{SLUG}}" aria-describedby="actions-{{SLUG}}">Find sampled minimum</button>
        <label class="shading-toggle"><input type="checkbox" id="btn-heat-{{SLUG}}" checked>Show mass shading</label>
      </div>
      <p class="hint" id="actions-{{SLUG}}">The net minimum is the least covered mass over all {{N_DIRECTIONS}} net directions; the button returns to its placement at direction 0.
      The sampled minimum searches a grid of centers at the current angle; it can miss smaller event cells.</p>
      <p class="hint control-status" id="status-{{SLUG}}" role="status" aria-live="polite" hidden></p>
      <div class="legend">
        <span><i style="background:var(--cert-near)"></i><span class="tex">1 \le \text{mass} &lt; {{TIGHT_JS}}</span></span>
        <span><i style="background:var(--kpress-doc-accent)"></i><span class="tex">\text{mass} \ge {{TIGHT_JS}}</span></span>
        <span><i style="background:var(--cert-below)"></i>mass below 1</span>
      </div>
      <p class="hint" id="hint-{{SLUG}}">Drag the orange square, or tap to place its center. Tap its round handle to turn by 5°, or drag it to rotate freely;
      the slider then shows the nearest net direction after square symmetry. Move the slider to return to the net.
      The shading samples the mass covered at each center position.
      The dashed outline bounds the allowed centers: outside it, the square extends beyond the container.
      At a net direction, every allowed placement covers mass at least 1. The preview uses floating-point geometry;
      the exact verifier decides which atoms lie on an edge.</p>
    </div>
  </div>
  <div class="fig-choose"><span class="screen-only caps">Certificate shown in all figures</span>{{CERT_TOGGLE}}</div>
  <figcaption><strong>Figure 5.</strong> Condition 5. The prover<span class="screen-only">: drag the square, watch the mass</span>.
  The exact certificate guarantees covered mass at least 1 throughout the dashed domain at every net direction.
  The shading previews this mass. Outside the domain, the square extends beyond the container.</figcaption>
</figure>

<!--END:FIGURE-->

## From a Continuum of Angles to {{N_DIRECTIONS}}

Take a unit square at any angle.
A quarter turn leaves a square unchanged, so its angle may be taken below $\pi/2$, and
the net covers only the arc $[0, \pi/4]$. A square whose angle lies past $\pi/4$ is
therefore first reflected across the container’s diagonal: the image is a unit square in
the container whose angle $\varphi$ is on the arc, and by Condition 1 it covers the same
mass. Let $\theta$ be the net angle nearest $\varphi$. A smaller square of side $B$ at
angle $\theta$, with the same center, covers no more mass than the unit square if it
fits inside it, because the weights are nonnegative.
So if every placement of the smaller square at a net angle covers mass at least 1, every
unit square at any angle does too.

It fits exactly when

$$
B\,(\cos d + \sin d) \;\le\; 1,
$$

where $d$ is the angle between the two, at most half the gap between two consecutive net
angles. Since $\cos d + \sin d \le 1 + \tan d$ on $[0,\pi/4)$, it is enough that

$$
B\,(1 + D) \;\lt\; 1, \qquad D \;=\; \max_k \frac{t_{k+1}-t_k}{1+t_k t_{k+1}} \;=\; \max_k \tan\frac{\theta_{k+1}-\theta_k}{2}.
$$

That is Condition 4, and it couples the two parameters: a coarser net widens the gaps,
forces $B$ smaller, and makes Condition 5 harder to meet.

The contradiction needs a little more than a fit.
Two packed squares may share an edge, so the smaller square has to lie in its unit
square’s *interior*, where no other square reaches.
It does: its width across the unit square, $B(\cos d + \sin d)$, is $B$ when $d = 0$,
and $B \lt 1$ because $B(1 + D) \le 1$ with $D \gt 0$; when $d \gt 0$ it is
$B\cos d\,(1 + \tan d) \lt B(1 + D) \le 1$, since then $\cos d \lt 1$. So the interior
of every unit square at any angle holds mass at least $1$, as the budget assumed.
Nothing there needed the inequality in Condition 4 to be strict, so the strict form the
verifier tests is a sufficient condition rather than a necessary one, and both
certificates meet it.

Each angle is carried as a rational half-tangent, $\theta_k = 2\arctan t_k$, so that

$$
\cos\theta = \frac{1-t^2}{1+t^2}, \qquad \sin\theta = \frac{2t}{1+t^2}
$$

are exact rationals and no angle is a floating-point number.
The net must reach $\pi/4$, the end of the arc that Condition 1 reflects every angle
onto. That is Condition 3, and since $\tan(\pi/8) = \sqrt{2}-1$ is irrational it too is
tested in rational form:

$$
t_K^{\,2} + 2t_K - 1 \;\ge\; 0 \quad\Longleftrightarrow\quad t_K \;\ge\; \tan\frac{\pi}{8}.
$$

<!--BEGIN:FIGURE-->

<figure class="apparatus" data-figure="6">
  <div class="split">
    <div class="stage"><canvas class="draggable" id="shrink-{{SLUG}}" width="800" height="800"></canvas></div>
    <div class="panel">
      <div class="ctl">
        <span class="caps">Unit square’s angle <span class="tex">\varphi</span></span>
        <input type="range" id="phi-{{SLUG}}" min="0" max="450" value="196" step="1" aria-label="Unit square angle">
      </div>
      <div class="ctl">
        <span class="caps">Net size <span class="tex">K</span></span>
        <div class="btns">
          <button class="knet" data-k="3" aria-pressed="true">3</button>
          <button class="knet" data-k="10">10</button>
          <button class="knet" data-k="30">30</button>
          <button class="knet" data-k="{{N_DIRECTIONS_MAX}}">{{N_DIRECTIONS_MAX}}, the real net</button>
        </div>
      </div>
      <dl class="kv">
        <dt><span class="tex">\varphi</span></dt><dd id="s-phi-{{SLUG}}"></dd>
        <dt>nearest <span class="tex">\theta</span></dt><dd id="s-theta-{{SLUG}}"></dd>
        <dt>mismatch <span class="tex">d</span></dt><dd id="s-d-{{SLUG}}"></dd>
        <dt>largest <span class="tex">D</span></dt><dd id="s-D-{{SLUG}}"></dd>
        <dt><span class="tex">B</span> admitted</dt><dd id="s-B-{{SLUG}}"></dd>
        <dt><span class="tex">B(\cos d + \sin d)</span></dt><dd class="hi" id="s-prod-{{SLUG}}"></dd>
      </dl>
      <p class="hint screen-only">Opens at <span class="tex">K = 3</span>, the coarsest net the figure offers, where Condition 4 admits only
      <span class="tex">B \lt {{K3_LIMIT_TEX}}</span> and the shrink is unmistakable. Tap the round handle to turn
      the unit square by 5°, or drag it to rotate freely. At
      <span class="tex">K = {{N_DIRECTIONS_MAX}}</span>, the net the proof uses, the two squares are
      indistinguishable.</p>
    </div>
  </div>
  <div class="fig-choose">{{CERT_TOGGLE}}</div>
  <figcaption><strong>Figure 6.</strong> Condition 4. The shrink that buys the finite net. The dark outline is the unit square at angle <span class="tex">\varphi</span>. Orange is the
  side-<span class="tex">B</span> square at the nearest net angle. The proof only ever asks about the orange one.
  The product <span class="tex">B(\cos d + \sin d)</span> must stay below 1. At <span class="tex">K = {{N_DIRECTIONS_MAX}}</span>, the net the proof uses, that
  product’s largest value, at the widest half-gap, is <span class="tex">{{SHRINK_PEAK_TEX}}</span> at <span class="tex">B = {{SHRINK_SIDE_TEX}}</span>, the side the figure
  uses: one seven-decimal step below the largest side Condition 4 admits, a step taken so that the strict inequality holds
  however the division falls, so the shrink shown is, to within that step, the least the net allows. At the certificate’s own
  side the product reaches <span class="tex">{{SHRINK_PEAK_CERT_TEX}}</span>.</figcaption>
</figure>

<!--END:FIGURE-->

<!--BEGIN:COARSENING-->

## What a Coarser Net Costs

We use the net from Massaccesi’s certificate: {{N_DIRECTIONS}} equally spaced
half-tangents, from $0$ to
<span class="math-reference">${{LIMIT_NUM}}/{{LIMIT_DEN}}$.[^massaccesi]</span> To price
a coarser net, hold a certificate’s atoms fixed, coarsen the net, set $B$ to a
seven-place value one step below the largest Condition 4 admits, and decide Condition 5
again.
Figure 7 does this for each certificate, and its caption says what halving the net
costs.

<!--BEGIN:FIGURE-->

<figure data-figure="7">
  <div class="chart kpress-diagram">
    <svg viewBox="0 0 700 238" role="img" aria-label="{{COARSEN_ALT}}">
      <g fill="var(--kpress-doc-muted)">
        <line x1="76" y1="56" x2="76" y2="160" stroke="var(--kpress-doc-muted)"/>
        <line x1="76" y1="160" x2="664" y2="160" stroke="var(--kpress-doc-muted)"/>
        <line x1="76" y1="56" x2="664" y2="56" stroke="var(--cert-probe)" stroke-dasharray="4 4" opacity=".8"/>
        <text x="68" y="60" text-anchor="end">1.0</text>
        <text x="68" y="112" text-anchor="end">0.5</text>
        <text x="68" y="164" text-anchor="end">0</text>
        <text x="84" y="20" fill="var(--cert-probe)">Condition 5 threshold</text>
      </g>
      <g>
        {{COARSEN_BARS}}
      </g>
      <g fill="var(--kpress-doc-text)" text-anchor="middle">
        {{COARSEN_VALUES}}
      </g>
      <g fill="var(--kpress-doc-muted)" text-anchor="middle">
        {{COARSEN_LABELS}}
      </g>
    </svg>
    <p class="figure-note">{{COARSEN_VERDICT}} Measured on the retained atoms, optimized against the full net.</p>
  </div>
  <div class="fig-choose">{{CERT_TOGGLE}}</div>
  <figcaption><strong>Figure 7.</strong> Condition 4 → Condition 5. Least covered mass as the net of the {{L_FRAC}} certificate is coarsened. Halving the net shrinks
  <span class="tex">B</span> by {{HALVING_B_DROP}} and costs {{HALVING_MASS_DROP}} of the least covered mass. This shows these atoms are tight
  against their own net, not that no coarser net could be made to work. It measures the slope of the trade.</figcaption>
</figure>

<!--END:FIGURE-->

<!--END:COARSENING-->

## The Contradiction Argument

<div class="boxed-text">

Take any packing of eleven unit squares in the side-{{L_DEC}} container.
Reflect across the container’s diagonal each square whose angle lies past $\pi/4$, so
that every angle is on the arc from $0$ to $\pi/4$ the net covers (Condition 3).

Each square then contains a side-$B$ square $Q_i$, centered at the same point and
oriented at the nearest net angle, inside the unit square’s interior: the mismatch $d$
of the two angles has $\tan d \le D$, and Condition 4 makes $B(\cos d + \sin d) \lt 1$
for every such $d$. Each $Q_i$ covers mass at least $1$, which is Condition 5.

Now reflect back each square that was reflected, and $Q_i$ with it.
$Q_i$ still lies in its own unit square’s interior, and by Condition 1 it still covers
mass at least $1$.

The unit squares have disjoint interiors, so the eleven $Q_i$ are disjoint.
Because the weights are nonnegative and no atom is counted twice, the eleven together
cover at most the container’s total mass.
Then

$$
{{N}} \;\le\; \sum_{i=1}^{{{N}}} \mu(Q_i) \;\le\; \mu\!\left([0,L]^2\right) \;=\; {{TOTAL_TEX}} \;=\; {{TOTAL_DEC}} \;\lt\; {{N}},
$$

where the last step is Condition 2. The two ends contradict each other, so no such
packing exists, and $s({{N}}) \ge {{L_FRAC}}$.

</div>

The argument shows that a container of side exactly {{L_FRAC}} is too small.
By compactness a packing exists at the infimum, so in fact $s({{N}}) \gt {{L_FRAC}}$;
the claim is stated as $\ge$ because that is what the theorem behind the verifier
proves, with no appeal to compactness.

## Beyond Point Atoms: The Current Bound

The point proof gives each site a weight and charges a core whenever it contains that
site. T-025 keeps that mechanism and adds **threshold atoms**. A threshold atom is a
finite set $S$, a threshold $k$, and a nonnegative weight $w$. It charges a core $w$
when the core contains at least $k$ points of $S$.

The budget changes with this rule.
The selected cores lie strictly inside packed squares, so they are pairwise disjoint.
Their traces on $S$ are therefore disjoint as well.
If $r$ cores trigger one threshold atom, then $rk \le |S|$, so that atom can charge at
most $\lfloor |S|/k\rfloor$ cores and costs $w\lfloor |S|/k\rfloor$ in the global
budget. A point atom is the special case $|S|=k=1$.

### T-025: an excluded endpoint at 3.82

The [T-025 certificate]({{T025_CERT_URL}}) has {{T025_POINT_ATOMS}} point atoms with
mass ${{T025_POINT_MASS}}$ and {{T025_THRESHOLD_ATOMS}} threshold atoms with budget
${{T025_THRESHOLD_BUDGET}}$. Every threshold atom is two-of-three, so it can charge at
most one of the disjoint cores.
The total budget is

$$
{{T025_TOTAL_BUDGET}} = {{T025_TOTAL_DEC}} < 11.
$$

An exact event-cell sweep over {{T025_DIRECTIONS}} net directions finds least charge
${{T025_LEAST_CHARGE}} > 1$. A separate interval calculation checks
{{T025_INTERVAL_DIRECTIONS}} canonical directions.
The same shrink-and-snap argument used above selects a legal core inside every physical
square, and the threshold budget then gives the same contradiction.
Thus T-025 excludes the endpoint $L={{CURRENT_ENDPOINT_FRAC}}={{CURRENT_ENDPOINT_DEC}}$.
The [retained proof packet]({{T025_PROOF_URL}}) gives the theorem, exact arithmetic, and
both verification routes.

### T-026: a finer net and a weak limit

A finer net reduces the largest angular mismatch and permits a larger core.
T-026 uses the same atom locations and thresholds on {{T026_DIRECTIONS}} directions,
raises the core side to $B={{T026_FINE_B}}$, and rescales every weight by one common
rational factor, ${{T026_NORMALIZATION}}$. Its least charge is exactly $1$, while its
total budget remains ${{T026_TOTAL_BUDGET}} = {{T026_TOTAL_DEC}} < 11$. A second method
checks all
{{T026_INTERVAL_DIRECTIONS}} directions.
These facts are recorded in the [finer-net certificate]({{T026_CERT_URL}}).

Now scale the container, the core, and every atom point together by a positive rational
factor $q$. Containment traces do not change, so neither the charge nor the budget
changes.
The sharper trigonometric containment test holds for every positive rational $q$
with $0<q<c$, where

$$
c = {{T026_FACTOR}}.
$$

It follows that every side below $(191/50)c$ is excluded.
Rational density and upward embedding then give

$$
s(11) \;\ge\; {{CURRENT_BOUND_TEX}} = {{CURRENT_BOUND_DEC}}.
$$

At $q=c$ the containment inequality becomes equality.
This limiting argument therefore does not supply a certificate at the displayed endpoint
or prove a strict lower bound.
For every positive rational $0<q<c$, however, it supplies an exact certificate at
$q(191/50)$, including rational sides above $3.82$. T-025 remains the reference
separately retained endpoint certificate at $3.82$. The
[T-026 proof]({{T026_PROOF_URL}}) and its
[machine-readable limit record]({{T026_RECORD_URL}}) carry the exact derivation.

## Generator and Verifier

The generator solves for the weights on a chosen set of sites $A$, arranged in orbits of
$\mathbf{D}_4$. The weights, one per orbit, come from the covering linear program

$$
\tau^*(A, \Theta; L, B) \;=\; \min_{w \,\ge\, 0}\; \sum_{a \in A} w_a \quad\text{subject to}\quad \sum_{a \in Q} w_a \;\ge\; 1 \;\;\text{ for every placement } Q,
$$

with one constraint per placement of a side-$B$ square at a direction of the net
$\Theta$. Placements form a continuum, so constraints are generated as needed: the
event-cell sweep that decides Condition 5 finds a placement whose mass falls short, and
it becomes a new constraint.
The sweep is the separation oracle.

Condition 1 holds by construction, Condition 5 is feasibility in this program, and
Condition 2 is a bound on its objective, so on a net and shrink that satisfy Conditions
3 and 4, a certificate on these sites exists when $\tau^* \lt n$. The target $n$ never
enters the program; it is compared with the optimum afterwards.
What the certificate carries is not that optimum but a rational point beside it: the
solver’s weights, inflated slightly and rounded up to multiples of ${{SCALE}}$ so that
every constraint holds in exact arithmetic.
The verifier proves that point feasible, not minimal.

The search runs in floating point.
None of it is part of the proof: the [generator]({{GENERATOR_URL}}) writes the
certificate to a file, and the [verifier]({{VERIFIER_URL}}) decides Conditions 1 through
5 on it in exact rational arithmetic.
The verifier rejects a certificate that fails the conditions, regardless of how it was
generated. The gate that admits a certificate to the record asks for two verdicts: it
accepts one only when the exact event-cell sweep and an interval branch-and-bound, which
decide Condition 5 by distinct methods, both accept it and report the same least covered
mass.

Geometric constraints can strengthen the final count.
Stromquist’s six-square proof rules out a container of side less than 3 by forcing four
of eight marked points into one square; each other square must contain at least one, so
at most five fit. The repaired eleven-square argument similarly forces three of twelve
points into one square.[^stromquist-memos][^repair] These examples suggest extending the
weighted method by using constraints between squares to force additional mass
consumption.

A [first-party package for third-party checking]({{THIRDPARTY_URL}}) gathers what an
outside check needs: the theorem written out, the {{THIRDPARTY_L_FRAC}} certificate as
plain data, and a one-file verifier on Python’s standard library that decides it without
importing anything else from the repository.

<!--BEGIN:COMPARISON-->

(It decides the looser of the two bounds, not the headline one.)

<!--END:COMPARISON-->

This project wrote every file in the package, so it is not itself a third-party check.

<!--BEGIN:CLAIM-->

## Verifiable Claim

Each point-certificate bound shown in the interactive figures has one self-contained
file: the claim, the theorem with its proof, a verifier in Python’s standard library,
and the certificate it decides, to paste into any coding agent or check by hand.

For $s(11) \ge {{HEADLINE_L_FRAC}}$:
[`{{HEADLINE_CLAIM_NAME}}`]({{HEADLINE_CLAIM_URL}}),
{{HEADLINE_N_ATOMS}} atoms.<!--BEGIN:COMPARISON--> (For the weaker bound
$s(11) \ge {{DEFAULT_L_FRAC}}$: [`{{DEFAULT_CLAIM_NAME}}`]({{DEFAULT_CLAIM_URL}}),
{{DEFAULT_N_ATOMS}} atoms.)<!--END:COMPARISON-->

The one-file checker [`minimal_verify.py`]({{PINNED_VERIFIER_URL}}) verifies the
{{HEADLINE_L_FRAC}} certificate in {{HEADLINE_PINNED_RUNTIME}}.[^verifier-timing]

The threshold certificates use the repository’s exact replay tools instead.
The [T-025 proof packet]({{T025_PROOF_URL}}) records its event-cell and interval checks;
the [T-026 proof]({{T026_PROOF_URL}}) gives the commands that decide the finer-net
certificate and re-derive its dilation limit.

<!--END:CLAIM-->

## Acknowledgments

We thank Walter Stromquist for drawing attention to his twenty-six-square construction
in Memo III (private communication, September 2026). His suggestion prompted a
[source review and independent exact verification]({{STROMQUIST_N26_REVIEW_URL}}).

## Further Reading

- **Papers and sources**
  - Friedman’s survey: an introduction to the problem and its literature.[^survey]
  - Stromquist’s geometric proofs for ten and eleven
    squares.[^stromquist-history][^stromquist-memos]
  - Nagamochi’s lower bounds for square packings in rectangles.[^lineage]
  - Burns’s weighted certificates and Massaccesi’s linear program for finding their
    weights.[^burns][^massaccesi]
  - [Full paper and source archive]({{ARCHIVE_URL}}): original papers, searchable
    transcriptions, and captured web sources
- **Elements of the project**
  - **[Project overview](https://github.com/jlevy/squares):** results, repository
    structure, and the research process
  - **[Problem tutorial]({{TUTORIAL_URL}}):** written as part of this project, a
    first-principles introduction to square packing, bounds, search, and proof
    obligations
  - **[Atlas of packings]({{ATLAS_URL}}):** created as part of this project, a
    collection of the best known packings for $n=1$ through $324$, with figures,
    geometry records, and provenance
- **Agentic research framework**
  - **[Workflows]({{WORKFLOWS_URL}})** define entry conditions and expected outputs for
    each kind of research work.
  - **[Operating principles]({{PRINCIPLES_URL}})** cover correctness, process, insight,
    and efficiency.
  - **[Epistemics]({{EPISTEMICS_URL}})** classifies results by verification,
    confirmation, significance, and novelty.
- **Agentic tooling**
  - **[tbd](https://github.com/jlevy/tbd):** tasks, dependencies, and handoffs tracked
    in Git, plus engineering best practices and guidelines for agents
  - **[Softschema](https://github.com/jlevy/softschema):** research records in YAML and
    Markdown, with validation rules that can become stricter as the work matures
- **Document tooling**
  - **[Practical Prose](https://github.com/jlevy/practical-prose):** writing guidelines,
    editing workflows, and document evaluation
  - **[Flowmark](https://github.com/jlevy/flowmark):** automated Markdown management and
    consistent formatting
  - **[KPress](https://github.com/jlevy/kpress):** web and print formatting from
    Markdown

[^stromquist-history]: Walter Stromquist states this bound in
    [Memo III ({{PRIOR_MEMO_YEAR}}), p. 10]({{PRIOR_MEMO_URL}}#page=10), as an
    adaptation of his preceding proof for $0^\circ$ and $45^\circ$ orientations.
    This suggests he already had the general argument, whose details he omits.
    The journal proof appeared in
    [Packing 10 or 11 unit squares in a square]({{PRIOR_URL}}), Electronic Journal of
    Combinatorics 10 ({{PRIOR_YEAR}}), R8.

[^stromquist-memos]: Walter Stromquist, *Packing Unit Squares Inside Squares*,
    [Memo I]({{PRIOR_SIX_MEMO_URL}}), September 11, 1984, pp.
    13–19, gives the six-square helper argument.
    [Memo II]({{PRIOR_TEN_MEMO_URL}}), October 15, 1984, proves the ten-square result,
    later published in his [{{PRIOR_YEAR}} paper]({{PRIOR_URL}}).

[^novelty]: Our
    [search through September 4, 2026]({{ARCHIVE_URL}}/web/s11-lower-bound-literature-audit-2026)
    found no earlier improvement on Stromquist’s bound, stated in {{PRIOR_MEMO_YEAR}}
    and published in {{PRIOR_YEAR}}. We checked the project’s sources, scholarly
    indexes, author pages, and public packing catalogues, but may have missed work in
    subscription-only indexes, theses, proceedings, or unindexed sources.

[^repair]: The bound is correct, but the project found that Stromquist’s printed
    argument does not close at his Figure 14 and repaired it with a source-distinct
    point set, certified exactly (`T-010` in the project’s result register).
    The proof here does not depend on it.

[^survey]: Erich Friedman,
    [Packing unit squares in squares: a survey and new results]({{PROBLEM_URL}}),
    Electronic Journal of Combinatorics, Dynamic Survey DS7.

[^trump]: Walter Trump’s packing of 1979, as recorded in
    [Kingbird’s register of squares in squares]({{BEST_URL}}), which also lists the
    degree-eight polynomial defining its side length.
    The [rendering]({{BEST_RENDER_URL}}) is the project’s own.
    Stromquist’s [Memo III]({{PRIOR_MEMO_URL}}), pp.
    2–4, credits Mats Gustafsson and Magnus Thulin with the same construction, reported
    by Gardner in November 1980; the research archive records their independent
    rediscovery.

[^other-results]: The [result register]({{RESULTS_URL}}) records $s(12) \ge 3.96$
    (`T-017`), $s(17) \ge 4.59$ (`T-019`), and $s(19) \ge 4.80$ (`T-020`), each
    supported by a retained weighted-point certificate and classified as apparently
    novel.

[^burns]: Sam Burns,
    [Proposing a Better Lower Bound for n=17 Square Packing](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/),
    August 2026, presents a weighted-point certificate for seventeen squares with a
    rational direction net and exact coverage checks.
    Burns credits ChatGPT with developing the certificate.

[^massaccesi]: Gustavo Massaccesi,
    [Another Better Lower Bound for n=17 Square Packing](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html),
    August 2026, improves Burns’s certificate.
    His
    [Linear Programing for Square Packing](https://gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html)
    describes the linear program and search used to find its weights.

[^lineage]: Earlier counting methods include Göbel’s unavoidable points and Nagamochi’s
    weighted resources: F. Göbel, Geometrical packing and covering problems, in *Packing
    and Covering in Combinatorics*, Mathematical Centre Tracts 106 (1979), 179–199;
    Hiroshi Nagamochi, [Packing unit squares in a rectangle]({{NAGAMOCHI_URL}}),
    Electronic Journal of Combinatorics 12 (2005), R37.

<!--BEGIN:CLAIM-->

[^verifier-timing]: The one-minute timing is for `minimal_verify.py`;
    [recorded runs]({{PROOF_CARD_URL}}#verify-it-in-one-command) took 47.5–67.0 seconds
    under CPython 3.14 on September 5, 2026. The claim document embeds a separate
    verifier, `verify_claim.py`, which checks the same certificate in
    {{HEADLINE_RUNTIME}} on an Apple Silicon laptop.

<!--END:CLAIM-->

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
