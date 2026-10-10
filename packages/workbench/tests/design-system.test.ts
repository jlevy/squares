import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync } from "node:fs";
import { join, relative } from "node:path";
import { test } from "node:test";
import type { CorpusFacts } from "../src/data/corpus.ts";
import { BADGE_LABELS, NEW_RESULT_BADGE, planFacts } from "../src/view/facts.ts";
import {
  type AllowEntry,
  type ContrastPair,
  checkContrast,
  contrastRatio,
  type InlineAllowEntry,
  inlineStyleFindings,
  matchInlineAllow,
  rawValueFindings,
  resolveToken,
  tokenBlock,
} from "../tools/design-contract.ts";

/**
 * The workbench's design system, held on the page's own files: every design value in the
 * stylesheet's token block, no inline style outside a counted allowance, and every text and
 * component colour pair at WCAG AA. `design-contract.test.ts` proves the machinery refuses what it
 * should; this applies it. The layout those tokens produce is measured in Chromium by
 * `workbench_tools.check_layout`.
 */
const PACKAGE = join(import.meta.dirname, "..");
const STYLESHEET = "assets/workbench.css";
const ALLOWLIST = "design-allowlist.json";

interface Allowlist {
  stylesheet: AllowEntry[];
  inlineStyles: InlineAllowEntry[];
}

function read(path: string): string {
  return readFileSync(join(PACKAGE, path), "utf8");
}

function allowlist(text: string): Allowlist {
  const parsed = JSON.parse(text) as Partial<Allowlist>;
  return { stylesheet: parsed.stylesheet ?? [], inlineStyles: parsed.inlineStyles ?? [] };
}

function sources(directory: string): string[] {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      return sources(path);
    }
    return /\.(?:ts|js)$/.test(entry.name) && !entry.name.endsWith(".d.ts") ? [path] : [];
  });
}

test("every design value in the stylesheet is a token", () => {
  const { findings, unusedAllow } = rawValueFindings(
    read(STYLESHEET),
    allowlist(read(ALLOWLIST)).stylesheet,
  );
  assert.deepEqual(
    findings.map((f) => `${STYLESHEET}:${f.line}: ${f.selector} { ${f.property}: ${f.value} }`),
    [],
    "declare the value in the :root token block and refer to it with var()",
  );
  assert.deepEqual(unusedAllow, [], "an allowance that matches nothing has to leave the list");
});

test("no inline style is written outside its counted allowance", () => {
  const files = [...sources(join(PACKAGE, "src")), join(PACKAGE, "assets/template.html")].map(
    (path) => ({
      path: relative(PACKAGE, path).split("\\").join("/"),
      text: readFileSync(path, "utf8"),
    }),
  );
  const { unallowed, stale } = matchInlineAllow(
    inlineStyleFindings(files),
    allowlist(read(ALLOWLIST)).inlineStyles,
  );
  assert.deepEqual(
    unallowed.map((f) => `${f.path}:${f.line}: ${f.property}: ${f.code}`),
    [],
    "move the value to a class or a custom property the stylesheet reads",
  );
  assert.deepEqual(stale, [], "a count that has fallen has to fall in the allowlist too");
});

test("the allowlist only shrinks against origin/main", (t) => {
  let previous: string;
  try {
    previous = execFileSync("git", ["show", `origin/main:packages/workbench/${ALLOWLIST}`], {
      cwd: PACKAGE,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    });
  } catch {
    t.diagnostic(`origin/main has no ${ALLOWLIST} to compare with; nothing to ratchet against`);
    return;
  }
  const before = allowlist(previous);
  const now = allowlist(read(ALLOWLIST));
  const rule = (e: AllowEntry): string => JSON.stringify([e.selector, e.property, e.value]);
  const known = new Set(before.stylesheet.map(rule));
  assert.deepEqual(
    now.stylesheet.filter((e) => !known.has(rule(e))).map(rule),
    [],
    "a stylesheet allowance origin/main does not have",
  );
  const counts = new Map(before.inlineStyles.map((e) => [`${e.path} ${e.property}`, e.count]));
  assert.deepEqual(
    now.inlineStyles
      .filter((e) => e.count > (counts.get(`${e.path} ${e.property}`) ?? 0))
      .map((e) => `${e.path} ${e.property}: ${e.count}`),
    [],
    "an inline style allowance above origin/main's count",
  );
});

test("every reason in the allowlist says something", () => {
  const { stylesheet, inlineStyles } = allowlist(read(ALLOWLIST));
  for (const entry of [...stylesheet, ...inlineStyles]) {
    assert.ok(entry.reason.trim().length >= 20, `a reason is a sentence: ${JSON.stringify(entry)}`);
  }
});

/**
 * The colour pairs the page draws. Text is 4.5:1 (WCAG 1.4.3). A control's boundary, the focus
 * rings, a chosen segment's fill and the stage's large type are 3:1 (1.4.11 and 1.4.3's large
 * text: the stage's heads are 28 px and its bound numbers 26 px bold in a 1080-line frame).
 */
const TEXT = 4.5;
const LARGE_OR_COMPONENT = 3;
const SURFACES = ["--color-page", "--color-surface"];
const PAIRS: ContrastPair[] = [
  ...["--color-text", "--color-text-label", "--color-text-muted"].flatMap((fg) =>
    [...SURFACES, "--color-surface-hover", "--color-surface-selected"].map((bg) => ({
      fg,
      bg,
      min: TEXT,
      role: "text on a surface",
    })),
  ),
  { fg: "--color-selected-text", bg: "--color-selected", min: TEXT, role: "a chosen segment" },
  { fg: "--color-selected-text", bg: "--color-accent", min: TEXT, role: "a primary button" },
  {
    fg: "--color-selected-text",
    bg: "--color-accent-hover",
    min: TEXT,
    role: "a primary button, hovered",
  },
  { fg: "--plot-text", bg: "--plot-field", min: TEXT, role: "the force law's labels" },
  {
    fg: "--color-text-label",
    bg: "--plot-field",
    min: TEXT,
    role: "the force law's push and pull",
  },
  ...SURFACES.flatMap((bg) => [
    { fg: "--color-border-control", bg, min: LARGE_OR_COMPONENT, role: "a control's boundary" },
    { fg: "--color-focus", bg, min: LARGE_OR_COMPONENT, role: "the focus ring" },
    { fg: "--color-focus-separator", bg, min: LARGE_OR_COMPONENT, role: "the separator's ring" },
    { fg: "--color-accent", bg, min: LARGE_OR_COMPONENT, role: "a primary button's fill" },
  ]),
  {
    fg: "--color-accent",
    bg: "--color-surface-selected",
    min: LARGE_OR_COMPONENT,
    role: "the showing tab's rule",
  },
  { fg: "--scene-ink", bg: "--scene-paper", min: TEXT, role: "stage text" },
  { fg: "--scene-label", bg: "--scene-paper", min: TEXT, role: "stage badge labels" },
  { fg: "--scene-heading", bg: "--scene-paper", min: LARGE_OR_COMPONENT, role: "stage heads" },
  { fg: "--scene-proved", bg: "--scene-paper", min: TEXT, role: "the proved lower bound" },
  { fg: "--scene-best", bg: "--scene-paper", min: TEXT, role: "the best known bound" },
  {
    fg: "--scene-frame",
    bg: "--scene-paper",
    min: LARGE_OR_COMPONENT,
    role: "the stage's frame",
  },
];

/**
 * The owner's frames, 2026-09-17: every outer container border the stage draws is one width --
 * the width the box already had -- and the only thing that changes between them is the colour.
 * The names are pinned to the chrome roles they take, and "medium" and "lightest" are pinned as
 * measurements rather than as words: against the page's white paper the trace is quieter than
 * the quietest line the chrome draws, and the frame sits between that line and the stage's ink.
 */
test("the stage's frames are one width in three named colours", () => {
  const block = tokenBlock(read(STYLESHEET));
  assert.ok(block !== null, "the stylesheet has no :root token block");
  const tokens = block.tokens;
  assert.equal(tokens.get("--scene-frame-width"), "4px");
  for (const [scene, role] of [
    ["--scene-frame", "--color-border-control"],
    ["--scene-frame-locked", "--color-status-best"],
    ["--scene-trace", "--color-divider"],
    ["--scene-proved", "--color-status-new"],
  ] as const) {
    assert.equal(
      resolveToken(scene, tokens),
      resolveToken(role, tokens),
      `${scene} is not ${role}`,
    );
  }
  const onPaper = (name: string): number =>
    contrastRatio(resolveToken(name, tokens), resolveToken("--scene-paper", tokens));
  assert.ok(
    onPaper("--scene-trace") < onPaper("--color-border"),
    "the trace is not the lightest line the page draws",
  );
  assert.ok(
    onPaper("--color-border") < onPaper("--scene-frame") &&
      onPaper("--scene-frame") < onPaper("--scene-ink"),
    "the frame's grey is not between the page's lines and its ink",
  );
});

test("every text and component colour pair meets WCAG AA", () => {
  const block = tokenBlock(read(STYLESHEET));
  assert.ok(block !== null, "the stylesheet has no :root token block");
  assert.deepEqual(
    checkContrast(block.tokens, PAIRS).map((f) => `${f.role}: ${f.fg} on ${f.bg} is ${f.ratio}`),
    [],
  );
});

function facts(overrides: Partial<CorpusFacts>): CorpusFacts {
  return {
    relation: "=",
    side: "4",
    exact: "4",
    exact_state: "closed-form",
    degree: 1,
    status: "proved",
    lower: null,
    kind: "square",
    badges: [{ glyph: "=", style: "solid", meaning: "exact value known" }],
    star: false,
    open: [],
    html_side: null,
    html_lower: null,
    html_headline: null,
    html_exact: null,
    ...overrides,
  };
}

test("a recent result is a `new result` star badge, first in the row", () => {
  const plan = planFacts(facts({ star: true, open: ["optimality"] }), 17);
  assert.deepEqual(plan.badges[0], { glyph: "★", style: "star", label: "new result" });
  assert.equal(BADGE_LABELS[`${NEW_RESULT_BADGE.glyph}/${NEW_RESULT_BADGE.style}`], "new result");
  assert.deepEqual(
    plan.badges.map((b) => b.label),
    ["new result", "exact"],
  );
  assert.deepEqual(
    planFacts(facts({ star: false, open: ["optimality"] }), 18).badges.map((b) => b.label),
    ["exact"],
  );
});

test("legacy and canonical rigidity badges share one dark R", () => {
  const plan = planFacts(
    facts({
      badges: [
        { glyph: "R", style: "muted", meaning: "annotated rigid by the catalogue" },
        { glyph: "R", style: "solid", meaning: "known rigid" },
      ],
    }),
    28,
  );
  assert.deepEqual(plan.badges, [{ glyph: "R", style: "solid", label: "rigid" }]);
});

test("OPEN is drawn only when something is open", () => {
  assert.equal(planFacts(facts({ open: [] }), 16).open, null);
  assert.deepEqual(planFacts(facts({ open: ["optimality", "rigidity"] }), 17).open, [
    { glyph: "?", style: "query", label: "optimality" },
    { glyph: "?", style: "query", label: "rigidity" },
  ]);
});

test("an unknown badge is refused rather than drawn unlabelled", () => {
  assert.throws(
    () => planFacts(facts({ badges: [{ glyph: "X", style: "solid", meaning: "?" }] }), 9),
    /unknown badge X\/solid for n = 9/,
  );
  assert.throws(
    () => planFacts(facts({ badges: [{ glyph: "R", style: "unknown", meaning: "?" }] }), 9),
    /unknown badge R\/unknown for n = 9/,
  );
});

test("negative controls: each contract refuses a regression written into the page's own files", () => {
  const css = read(STYLESHEET);
  const smuggled = `${css}\n#controls {\n  padding: 14px;\n  color: #8a939e;\n}\n`;
  assert.deepEqual(
    rawValueFindings(smuggled, [])
      .findings.map((f) => `${f.property}: ${f.value}`)
      .sort(),
    ["color: #8a939e", "padding: 14px"],
  );

  const application = "src/application.js";
  const written = `${read(application)}\ncontrols.style.padding = "14px";\n`;
  const { unallowed } = matchInlineAllow(
    inlineStyleFindings([{ path: application, text: written }]),
    allowlist(read(ALLOWLIST)).inlineStyles,
  );
  assert.deepEqual(
    unallowed.map((f) => f.property),
    ["padding"],
  );

  const block = tokenBlock(css);
  assert.ok(block !== null);
  // The quiet grey the chrome's small capitals used to be set in, 2.54:1 on the page.
  const quiet = new Map(block.tokens).set("--color-text-muted", "#8a939e");
  assert.ok(
    checkContrast(quiet, PAIRS).some(
      (f) => f.fg === "--color-text-muted" && f.bg === "--color-page",
    ),
  );
  // And the control border it replaced, 1.5:1.
  const faint = new Map(block.tokens).set("--color-border-control", "#b9c0c8");
  assert.ok(checkContrast(faint, PAIRS).some((f) => f.fg === "--color-border-control"));
});
