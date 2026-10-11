// Script class: Registered forwarder exception (404 aliases only).
// Resolve only retained case/result registrations, always under the project root.
(() => {
  const root = document.documentElement.dataset.siteRoot;
  const node = document.getElementById("site-url-aliases");
  if (!root || !node?.textContent || !location.pathname.startsWith(root)) {
    return;
  }
  /** @type {{cases: number[], results: string[], rows: string[], allResults: string | null}} */
  const aliases = JSON.parse(node.textContent);
  const path = location.pathname.slice(root.length);
  let target = null;
  const caseMatch = /^cases\/(?:n-)?0*(\d+)\.html$/.exec(path);
  const resultMatch = /^result\/[Tt]-(\d{3})\.html$/.exec(path);
  if (caseMatch && aliases.cases.includes(Number(caseMatch[1]))) {
    target = `cases/${Number(caseMatch[1])}.html`;
  } else if (resultMatch) {
    const result = `result/t-${resultMatch[1]}.html`;
    if (aliases.results.includes(result) && result !== path) {
      target = result;
    } else if (aliases.allResults && aliases.rows.includes(`t-${resultMatch[1]}`)) {
      target = `${aliases.allResults}#t-${resultMatch[1]}`;
    }
  }
  if (!target || target === path) {
    return;
  }
  const destination = new URL(root + target, location.origin);
  destination.search = location.search;
  if (!destination.hash) {
    destination.hash = location.hash;
  }
  location.replace(destination.href);
})();
