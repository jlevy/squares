// Input response and registered forwarding: moved pages preserve query and fragment.
// The overview forwards only the frozen explainer-era anchor inventory. Unknown
// fragments remain on this page; its own current anchors take precedence.
(() => {
  const explainerAnchors = new Set([
    "19-5",
    "381-100",
    "acknowledgments",
    "actions-19-5",
    "actions-381-100",
    "atoms-mass-and-the-budget",
    "beyond-point-atoms-the-current-bound",
    "btn-heat-19-5",
    "btn-heat-381-100",
    "btn-scan-19-5",
    "btn-scan-381-100",
    "btn-tight-19-5",
    "btn-tight-381-100",
    "every-placement-covers-mass-at-least-one",
    "field-19-5",
    "field-381-100",
    "field-tip-19-5",
    "field-tip-381-100",
    "figure-description",
    "figure-title",
    "fn-1",
    "fn-10",
    "fn-11",
    "fn-2",
    "fn-3",
    "fn-4",
    "fn-5",
    "fn-6",
    "fn-7",
    "fn-8",
    "fn-9",
    "fnref-1",
    "fnref-10",
    "fnref-10-2",
    "fnref-11",
    "fnref-2",
    "fnref-2-2",
    "fnref-3",
    "fnref-3-2",
    "fnref-4",
    "fnref-5",
    "fnref-6",
    "fnref-6-2",
    "fnref-7",
    "fnref-7-2",
    "fnref-7-3",
    "fnref-8",
    "fnref-8-2",
    "fnref-9",
    "fnref-9-2",
    "fnref-9-3",
    "from-a-continuum-of-angles-to-181",
    "further-reading",
    "generator-and-verifier",
    "hint-19-5",
    "hint-381-100",
    "kslider-19-5",
    "kslider-381-100",
    "kval-19-5",
    "kval-381-100",
    "md-19-5",
    "md-381-100",
    "mv-19-5",
    "mv-381-100",
    "new-lower-bounds-for-square-packing-for-n--11",
    "panel-0",
    "panel-0-fills",
    "panel-0-outlines",
    "phi-19-5",
    "phi-381-100",
    "proof",
    "proof-of-the-new-lower-bound",
    "prove-19-5",
    "prove-381-100",
    "s-B-19-5",
    "s-B-381-100",
    "s-D-19-5",
    "s-D-381-100",
    "s-d-19-5",
    "s-d-381-100",
    "s-phi-19-5",
    "s-phi-381-100",
    "s-prod-19-5",
    "s-prod-381-100",
    "s-theta-19-5",
    "s-theta-381-100",
    "shrink-19-5",
    "shrink-381-100",
    "status-19-5",
    "status-381-100",
    "t-025-a-direct-certificate-at-382",
    "t-026-finer-directions-and-the-new-lower-bound",
    "the-agentic-research-framework",
    "the-atom-set",
    "the-contradiction-argument",
    "the-five-conditions-for-a-point-certificate",
    "the-result-and-proof-roadmap",
    "the-square-packing-problem",
    "vd-19-5",
    "vd-381-100",
    "verifiable-claim",
    "version-history",
    "what-a-coarser-net-costs",
  ]);
  /** @param {string} target */
  const forward = (target) => {
    window.location.replace(`${target}${window.location.search}${window.location.hash}`);
  };
  const moved = document.documentElement.dataset.movedTo;
  if (moved) {
    const known = document.documentElement.dataset.caseNumbers;
    if (known) {
      const url = new URL(window.location.href);
      const query = url.searchParams.get("n");
      const fragment = /^#n-(\d+)$/.exec(url.hash)?.[1];
      const digits = query !== null && /^\d+$/.test(query) ? query : fragment;
      const n = digits === undefined ? "" : String(Number(digits));
      if (known.split(",").includes(n)) {
        url.searchParams.delete("n");
        const hash = fragment === undefined ? url.hash : "";
        window.location.replace(`cases/${n}.html${url.search}${hash}`);
        return;
      }
    }
    const fileTarget = document.documentElement.dataset.fileMovedTo;
    forward(window.location.protocol === "file:" && fileTarget ? fileTarget : moved);
    return;
  }
  const fragment = window.location.hash.slice(1);
  if (!fragment) {
    return;
  }
  let id = fragment;
  try {
    id = decodeURIComponent(fragment);
  } catch {
    // A malformed escape cannot name an element here either.
  }
  if (document.getElementById(id)) {
    return;
  }
  const all = document.querySelector("[data-all-results]");
  const retired = (() => {
    try {
      const aliases = JSON.parse(all?.getAttribute("data-retired-results") ?? "{}");
      return /^t-\d+$/.test(id) && Object.hasOwn(aliases, id) && aliases[id] === `result/${id}.html`
        ? aliases[id]
        : null;
    } catch {
      return null;
    }
  })();
  if (retired) {
    forward(retired);
    return;
  }
  const registered = (all?.getAttribute("data-result-ids") ?? "").split(/\s+/);
  const result =
    id === "every-result" ||
    id === "verification-ladders" ||
    id === "verification-at-a-glance" ||
    registered.includes(id);
  if (result) {
    forward("all-results.html");
  } else if (id === "the-frontier-survey" || id === "the-survey") {
    forward("frontier.html");
  } else if (explainerAnchors.has(id)) {
    forward("papers/n11-lower-bounds-explainer.html");
  }
})();
