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
  <a class="chip" href="{{REPO_URL}}" title="The project on GitHub"><svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>PROJECT</a>
</div>

<div class="hero">

# <span class="symbol">s({{N}}) <span class="rel">≥</span> {{HEADLINE_L_FRAC}}</span>

<p class="subtitle centred">{{SUBTITLE}}</p>

<div class="credits centred">
  <span>{{PUBLISHED}} ({{EDITION}})</span>
  <span>Tooling and human oversight: <a href="https://x.com/ojoshe"><strong>Joshua Levy</strong></a></span>
  <span>Agents: <strong>Opus 5</strong>, <strong>Fable 5.1</strong>, and <strong>Codex 5.6</strong></span>
  <span>Open source at <a href="https://github.com/jlevy/squares"><strong>github.com/jlevy/squares</strong></a></span>
</div>

</div>

## What Is This?

This paper presents a new lower bound on a long-standing open geometry problem: eleven
unit squares with disjoint interiors, free to rotate, cannot fit in a
${{HEADLINE_L_DEC}} \times {{HEADLINE_L_DEC}}$ square.

The computer-assisted proof was found via an automated research framework.
This is one of {{N_RESULTS}} results the framework has registered so far, {{N_NOVEL}} of
them apparently new.
The certificate used in the proof places {{HEADLINE_N_ATOMS}} rationally weighted points
in the container and selects a net of {{HEADLINE_N_DIRECTIONS}} rationally parameterized
directions. Five exact conditions and a pigeonhole-style argument then imply the claim.

<!--BEGIN:CLAIM-->

Verification is exact rational arithmetic: the one-file checker,
{{PINNED_VERIFIER_LINES}}
of standard-library Python and short enough to read in one sitting, decides the
certificate file of {{HEADLINE_N_ATOMS}} weighted points in {{HEADLINE_PINNED_RUNTIME}}.

<!--END:CLAIM-->

This appears to be the first improvement in {{YEARS_SINCE_PRIOR}} years on the smallest
open case of the square packing problem.[^novelty] The previous bound,
{{PRIOR_LOWER_DEC}}, was Stromquist’s in
{{PRIOR_YEAR}}.[^stromquist][^repair]

The search, the checking, and the record are the work of agents following a flexible but
defined research framework, available in
[the GitHub repository](https://github.com/jlevy/squares).
The atlas of best known packings for every $n$ from 1 to 100 in Figure 1 came from the
same research agenda and currently includes {{N_STARRED}} new lower bounds.

The repository holds much more than this proof: it includes a comprehensive survey of
previous research, the atlas of packings, a hypothesis registry, an experiment ledger,
exact verifiers, and a retention gate that labels results according to epistemic status
(levels of verification, confirmation, and significance).
Work is planned on a regular cadence (such as 8 to 12 hours) and broken into several
defined workflows (research survey, correctness verification, research loop,
optimization loop, and a few others).

The research framework itself is not specific to square packing.
It uses a few tools to streamline the process, notably
[tbd](https://github.com/jlevy/tbd) for task tracking,
[Softschema](https://github.com/jlevy/softschema) for structuring results, and
[Practical Prose](https://github.com/jlevy/practical-prose) to improve writing quality.

Every file in the repository (including this paper) is agent written.
The research framework’s structure had high-level human direction.
Similarly structured research frameworks are likely useful for creative mathematical or
technical problems of other sorts.

## The Square Packing Problem

The **square packing problem** asks, for each $n$, for the side $s(n)$ of the smallest
square that holds $n$ unit squares, which are free to rotate and must have disjoint
interiors.[^survey] The value of $s(n)$ is known for $n \le 10$. Stromquist settled
$s(10) = 3 + 1/\sqrt{2}$ in {{PRIOR_YEAR}}.[^stromquist]

<figure>
  <div class="stage"><a href="known-best-1-100.pdf"><img src="known-best-1-100.svg" alt="{{COMPOSITE_ALT}}" width="2400" height="2896"></a></div>
  <figcaption><strong>Figure 1.</strong> The best known packings of 1 through 100 unit squares. Each cell is the tightest
  arrangement on record for that <span class="tex">n</span>, with the best known upper bound beneath it and, where
  <span class="tex">s(n)</span> is not yet settled, the best proved lower bound below that. A crimson star marks a lower
  bound this project proved: {{N_STARRED}} of the hundred, this page’s own among them. The full
  results, with every witness and its provenance, are in
  <a href="{{ATLAS_URL}}">the GitHub repository</a>, and the
  composite is <a href="known-best-1-100.pdf">available as a PDF</a>.</figcaption>
</figure>

## Packing 11 Squares

$s(11)$ is the smallest case still open.
Trump’s 1979 packing shows $s(11) \le {{BEST_PACKING_TEX}}$.[^trump] Here we prove
$s(11) \ge {{HEADLINE_L_FRAC}} = {{HEADLINE_L_DEC}}$. A second certificate, for the
looser bound $s({{N}}) \ge {{DEFAULT_L_FRAC}}$, is kept beside it: its smaller numbers
make the figures legible, and it is the one the project’s adversarial review of the
checking package read line by line.
The {{HEADLINE_L_FRAC}} certificate supersedes it, and some of the figures below show
both.

<figure>
  <div class="stage trump"><a href="{{BEST_RENDER_URL}}" aria-label="The rendering in the repository">{{TRUMP_SVG}}</a></div>
  <figcaption><strong>Figure 2.</strong> Trump’s 1979 packing of eleven unit squares shows
  <span class="tex">s(11) \le {{BEST_PACKING_TEX}}</span>.</figcaption>
</figure>

<figure>
  <div class="line-fig kpress-diagram">
  <svg viewBox="0 0 700 92" role="img" aria-label="Number line from 3.75 to 3.90 showing the previous lower bound {{PRIOR_LOWER_DEC}}, the bounds proved here up to {{HEADLINE_L_DEC}}, and the best known packing at {{BEST_PACKING_DEC}}">
    <rect x="{{BAND_X}}" y="45" width="{{BAND_W}}" height="13" fill="var(--cert-accent-wash)"/>
    <line x1="20" y1="51.5" x2="680" y2="51.5" stroke="var(--kpress-doc-muted)" stroke-width="1"/>
    <g stroke="var(--kpress-doc-muted)" stroke-width="1">
      <line x1="20" y1="47" x2="20" y2="56"/><line x1="460" y1="47" x2="460" y2="56"/>
      <line x1="680" y1="47" x2="680" y2="56"/>
    </g>
    <g font-size="10" fill="var(--kpress-doc-muted)" text-anchor="middle">
      <text x="20" y="72">3.75</text><text x="460" y="72">3.85</text><text x="680" y="72">3.90</text>
    </g>
    <line x1="{{PRIOR_X}}" y1="30" x2="{{PRIOR_X}}" y2="51.5" stroke="var(--kpress-doc-muted)" stroke-width="1.25"/>
    <circle cx="{{PRIOR_X}}" cy="51.5" r="3.2" fill="var(--kpress-doc-muted)"/>
    <g text-anchor="middle">
      <text x="{{PRIOR_X}}" y="24" font-size="10.5" fill="var(--kpress-doc-text)">{{PRIOR_LOWER_DEC}}</text>
      <text x="{{PRIOR_X}}" y="12" font-size="9.5" fill="var(--kpress-doc-muted)">{{PRIOR_SOURCE}}</text>
      <text x="{{BEST_X}}" y="24" font-size="10.5" fill="var(--kpress-doc-text)">{{BEST_PACKING_DEC}}</text>
      <text x="{{BEST_X}}" y="12" font-size="9.5" fill="var(--kpress-doc-muted)">{{BEST_SOURCE}}</text>
    </g>
    <line x1="{{BEST_X}}" y1="30" x2="{{BEST_X}}" y2="51.5" stroke="var(--kpress-doc-muted)" stroke-width="1.25"/>
    <circle cx="{{BEST_X}}" cy="51.5" r="3.2" fill="var(--kpress-doc-muted)"/>
    {{NUMBER_LINE_MARKS}}
  </svg>
  </div>
  <figcaption><strong>Figure 3.</strong> Bounds on <span class="tex">s(11)</span>. The shaded band is the bound gap, what remains unknown about <span class="tex">s(11)</span>. With the lower bound at <span class="tex">{{HEADLINE_L_FRAC}}</span> the gap is
  <span class="tex">{{GAP_NOW}}</span> wide, down from <span class="tex">{{GAP_BEFORE}}</span> at Stromquist’s bound.</figcaption>
</figure>

## The Five Conditions

The argument is the weighted, fractional form of the classical unavoidable-set argument
for square packing, in the shape Gustavo Massaccesi used for $n = 17$ in August 2026
after Sam Burns proposed the weighted form,[^burns][^massaccesi] descended from Göbel’s
unavoidable points (1979) and Nagamochi’s weighted resources (2005).[^lineage] Neither
the theorem nor the shape of the certificate is this project’s; what is new here is the
$n = 11$ instance and the generator that found it.

The proof is a **certificate**: for $n$ unit squares in a container of side $L$, a
finite set of points in the container, each with a nonnegative rational weight (the
atoms; every weight in this certificate is positive), a net of directions
$\theta_k = 2\arctan t_k$ with rational half-tangents
$0 = t_0 \lt t_1 \lt \cdots \lt t_K$, and a shrink $B$, such that:

<div class="conditions boxed-text">

**Condition 1.** The atom set is invariant under the container’s symmetry group
$\mathbf{D}_4$, its four rotations and four reflections.

**Condition 2.** The total mass of the atoms, the sum of all their weights, is strictly
below $n$.

**Condition 3.** The net reaches $\pi/4$: its last half-tangent is at least
$\tan(\pi/8)$.

**Condition 4.** $B(1 + D) \lt 1$, where $D$ is the largest of the net’s half-gap
tangents, each the tangent of half the angle between two consecutive net directions.

**Condition 5.** At every net direction, every placement of a square of side $B$ inside
the container covers mass at least $1$.

</div>

Conditions 1 to 4 are exact rational comparisons.
Condition 5 is one exact sweep per direction.
Together the five prove $s(n) \ge L$. The two certificates are
[`{{DEFAULT_ID}}`]({{DEFAULT_CERT_URL}}) and [`{{ID}}`]({{CERT_URL}}), and every figure
below is [computed]({{RENDERER_URL}}) from the one it shows.

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

<figure data-figure="4">
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
  <figcaption><strong>Figure 4. Conditions 1 and 2.</strong> The atoms. Disc area is proportional to weight. Mass gathers along the edges and in a ring inside the
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

<figure data-figure="5">
  <div class="split">
    <div class="stage"><canvas class="draggable" id="prove-{{SLUG}}" width="1000" height="1000"></canvas></div>
    <div class="panel">
      <div class="readout">
        <span class="caps">Mass covered</span>
        <div class="mass-row">
          <div class="mass-val" id="mv-{{SLUG}}"></div>
          <div class="mass-dec" id="md-{{SLUG}}"></div>
        </div>
        <span class="verdict ok" id="vd-{{SLUG}}">Covers <span class="rel">≥</span> 1</span>
      </div>
      <div class="ctl">
        <span class="caps">Direction <span class="tex">k</span> of the {{N_DIRECTIONS}}-point net</span>
        <input type="range" id="kslider-{{SLUG}}" min="0" max="{{N_DIRECTIONS_MAX}}" value="0" step="1" aria-label="Net direction index">
        <div class="val" id="kval-{{SLUG}}"></div>
      </div>
      <div class="btns">
        <button id="btn-tight-{{SLUG}}">Tightest placement</button>
        <button id="btn-scan-{{SLUG}}">Scan this direction</button>
        <button id="btn-heat-{{SLUG}}" aria-pressed="true">Field</button>
      </div>
      <div class="legend">
        <span><i style="background:var(--cert-near)"></i>within {{TIGHT_PERCENT}}% of the limit</span>
        <span><i style="background:var(--kpress-doc-accent)"></i>comfortably above</span>
        <span><i style="background:var(--cert-below)"></i>below 1, which never occurs at a net direction</span>
      </div>
      <p class="hint" id="hint-{{SLUG}}">The shaded background is the covered mass at every center position, recomputed
      for the direction you choose. The dashed outline is where the square’s center is allowed to be. Outside
      it the square hangs out of the container, and the proof makes no claim.</p>
    </div>
  </div>
  <div class="fig-choose">{{CERT_TOGGLE}}</div>
  <figcaption><strong>Figure 5. Condition 5.</strong> The prover<span class="screen-only">: drag the square, watch the mass</span>. Inside the dashed domain the field never drops below 1, at any of the {{N_DIRECTIONS}}
  directions. Outside it the mass falls away at once, which is why the atoms crowd the boundary.</figcaption>
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

<figure data-figure="6">
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
      <span class="tex">B \lt {{K3_LIMIT_TEX}}</span> and the shrink is unmistakable. Drag either square by its
      handle. At
      <span class="tex">K = {{N_DIRECTIONS_MAX}}</span>, the net the proof uses, the two squares are
      indistinguishable.</p>
    </div>
  </div>
  <div class="fig-choose">{{CERT_TOGGLE}}</div>
  <figcaption><strong>Figure 6. Condition 4.</strong> The shrink that buys the finite net. The dark outline is the unit square at angle <span class="tex">\varphi</span>. Orange is the
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

The net was not derived here.
It is the one Massaccesi’s $n = 17$ certificate used, {{N_DIRECTIONS}} half-tangents
equally spaced from $0$ to ${{LIMIT_NUM}}/{{LIMIT_DEN}}$, carried over unchanged.
To price a coarser net, hold a certificate’s atoms fixed, coarsen the net, set $B$ to a
seven-place value one step below the largest Condition 4 admits, and decide Condition 5
again.
Figure 7 does this for each certificate, and its caption says what halving the net
costs.

<!--BEGIN:FIGURE-->

<figure data-figure="7">
  <div class="chart kpress-diagram">
    <svg viewBox="0 0 700 250" role="img" aria-label="{{COARSEN_ALT}}">
      <g font-size="10" fill="var(--kpress-doc-muted)">
        <line x1="76" y1="30" x2="76" y2="190" stroke="var(--kpress-doc-muted)"/>
        <line x1="76" y1="190" x2="664" y2="190" stroke="var(--kpress-doc-muted)"/>
        <line x1="76" y1="30" x2="664" y2="30" stroke="var(--cert-probe)" stroke-dasharray="4 4" opacity=".8"/>
        <text x="68" y="34" text-anchor="end">1.0</text>
        <text x="68" y="114" text-anchor="end">0.5</text>
        <text x="68" y="194" text-anchor="end">0</text>
        <text x="84" y="24" fill="var(--cert-probe)">Condition 5 threshold</text>
      </g>
      <g>
        {{COARSEN_BARS}}
      </g>
      <g font-size="10.5" fill="var(--kpress-doc-text)" text-anchor="middle">
        {{COARSEN_VALUES}}
      </g>
      <g font-size="10.5" fill="var(--kpress-doc-muted)" text-anchor="middle">
        {{COARSEN_LABELS}}
      </g>
      <text x="76" y="246" font-size="10" fill="var(--kpress-doc-muted)">
        {{COARSEN_VERDICT}} Measured on the retained atoms, optimized against the full net.
      </text>
    </svg>
  </div>
  <div class="fig-choose">{{CERT_TOGGLE}}</div>
  <figcaption><strong>Figure 7. Condition 4 <span class="rel">→</span> Condition 5.</strong> Least covered mass as the net of the {{L_FRAC}} certificate is coarsened. Halving the net shrinks
  <span class="tex">B</span> by {{HALVING_B_DROP}} and costs {{HALVING_MASS_DROP}} of the least covered mass. This shows these atoms are tight
  against their own net, not that no coarser net could be made to work. It measures the slope of the trade.</figcaption>
</figure>

<!--END:FIGURE-->

<!--END:COARSENING-->

## The Contradiction

<div class="boxed-text">

Take any packing of eleven unit squares in the side-{{L_DEC}} container.
Reflect across the container’s diagonal each square whose angle lies past $\pi/4$, so
that every angle is on the arc from $0$ to $\pi/4$ the net covers (Condition 3). Each
square then contains a side-$B$ square $Q_i$, centered at the same point and oriented at
the nearest net angle, inside the unit square’s interior: the mismatch $d$ of the two
angles has $\tan d \le D$, and Condition 4 makes $B(\cos d + \sin d) \lt 1$ for every
such $d$. Each $Q_i$ covers mass at least $1$, which is Condition 5. Now reflect back
each square that was reflected, and $Q_i$ with it.
$Q_i$ still lies in its own unit square’s interior, and by Condition 1 it still covers
mass at least $1$. The unit squares have disjoint interiors, so the eleven $Q_i$ are
disjoint. Because the weights are nonnegative and no atom is counted twice, the eleven
together cover at most the container’s total mass.
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

## Generator and Verifier

The atoms are solved for, not placed by hand.
The sites $A$ are fixed in advance, in orbits of $\mathbf{D}_4$, and the weights, one
per orbit, come from the covering linear program

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
A certificate written by a wrong program is rejected by the verifier.
The gate that admits a certificate to the record asks for two verdicts: it accepts one
only when the exact event-cell sweep and an interval branch-and-bound, which decide
Condition 5 by distinct methods, both accept it and report the same least covered mass.

A [first-party package for third-party checking]({{THIRDPARTY_URL}}) gathers what an
outside check needs: the theorem written out, the {{DEFAULT_L_FRAC}} certificate as
plain data, and a one-file verifier on Python’s standard library that decides it without
importing anything else from the repository.
It decides the looser of the two bounds, not the headline one, and since this project
wrote every file in it, it is not itself a third-party check.

<!--BEGIN:CLAIM-->

## Verifiable Claim

Each bound has one self-contained file: the claim, the theorem with its proof, a
verifier in Python’s standard library, and the certificate it decides, to paste into any
coding agent or check by hand.

- $s(11) \ge {{DEFAULT_L_FRAC}}$: [`{{DEFAULT_CLAIM_NAME}}`]({{DEFAULT_CLAIM_URL}}),
  {{DEFAULT_N_ATOMS}} atoms, verified in {{DEFAULT_RUNTIME}}.
- $s(11) \ge {{HEADLINE_L_FRAC}}$: [`{{HEADLINE_CLAIM_NAME}}`]({{HEADLINE_CLAIM_URL}}),
  {{HEADLINE_N_ATOMS}} atoms, verified in {{HEADLINE_RUNTIME}}.

The times are the embedded verifier’s, on a laptop.
The one-file checker beside it that pins the certificate’s digest, `minimal_verify.py`,
decides the {{HEADLINE_L_FRAC}} certificate in {{HEADLINE_PINNED_RUNTIME}}.

<!--END:CLAIM-->

[^stromquist]: Walter Stromquist,
    [Packing 10 or 11 unit squares in a square]({{PRIOR_URL}}), Electronic Journal of
    Combinatorics 10 (2003), R8.

[^novelty]: No improvement on Stromquist’s {{PRIOR_YEAR}} bound is known to us.
    The search behind that statement, recorded in the repository, covered the project’s
    literature archive and source register, then arXiv, Crossref, OpenAlex and Semantic
    Scholar, author pages and the public packing catalogues, through September 4, 2026.
    It did not exhaust subscription-only indexes, theses and proceedings, or unindexed
    sources. The claim is apparent novelty within the searched public record, not
    priority.

[^repair]: The bound is correct, but the project found that Stromquist’s printed
    argument does not close at his Figure 14 and repaired it with a source-distinct
    point set, certified exactly (`T-010` in the project’s result register).
    The proof here does not depend on it.

[^survey]: Erich Friedman,
    [Packing unit squares in squares: a survey and new results]({{PROBLEM_URL}}),
    Electronic Journal of Combinatorics, Dynamic Survey DS7.

[^trump]: Walter Trump’s packing of 1979, as recorded in
    [Kingbird’s register of squares in squares]({{BEST_URL}}). The
    [rendering]({{BEST_RENDER_URL}}) is the project’s own.

[^burns]: Sam Burns,
    [Proposing a Better Lower Bound for n=17 Square Packing](https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/),
    August 2026.

[^massaccesi]: Gustavo Massaccesi,
    [Another Better Lower Bound for n=17 Square Packing](https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html),
    August 2026, with the linear program that found it described in
    [a companion post](https://gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html).

[^lineage]: F. Göbel, Geometrical packing and covering problems, in *Packing and
    Covering in Combinatorics*, Mathematical Centre Tracts 106 (1979), 179–199; Hiroshi
    Nagamochi, Packing unit squares in a rectangle, Electronic Journal of Combinatorics
    12 (2005), R37.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
