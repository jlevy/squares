// Facets enhance a News list. The archive filters every article and keeps the choice in
// its address; without scripts no article is filtered out there. A preview, the home
// page's News box (`data-news-limit`), shows the newest articles that match, up to its
// limit, says how many in its live count, keeps no address and carries the choice on
// its "View All News" link (`data-news-carry`). Either opens on the levels its markup
// presses.
(() => {
  const controls = document.querySelector("[data-news-filters]");
  const news = document.querySelector("[data-news]");
  if (!(controls instanceof HTMLElement) || !(news instanceof HTMLElement)) {
    return;
  }
  const cards = [...news.querySelectorAll("[data-news-day]")].filter(
    (card) => card instanceof HTMLElement,
  );
  const scoreButtons = [...controls.querySelectorAll("button[data-news-score]")];
  const topicButtons = [...controls.querySelectorAll("button[data-news-topic]")];
  const allScores = scoreButtons.map((button) => button.getAttribute("data-news-score") || "");
  const allTopics = topicButtons.map((button) => button.getAttribute("data-news-topic") || "");
  // The levels the page opens on, which an address without `news-s` means.
  const initial = scoreButtons
    .filter((button) => button.getAttribute("aria-pressed") === "true")
    .map((button) => button.getAttribute("data-news-score") || "");
  const limit = Number.parseInt(news.dataset.newsLimit || "", 10);
  const preview = limit > 0;
  let scores = new Set(initial);
  let topics = new Set(allTopics);
  /** @param {string} name @param {string[]} allowed @param {string[]} fallback */
  const read = (name, allowed, fallback) => {
    const value = new URL(location.href).searchParams.get(name);
    return new Set(
      value === null ? fallback : value.split(",").filter((item) => allowed.includes(item)),
    );
  };
  const restore = () => {
    scores = read("news-s", allScores, initial);
    topics = read("news-topics", allTopics, allTopics);
  };
  /** @param {HTMLElement} card */
  const subjects = (card) => (card.dataset.newsTopics || "").split(" ").filter(Boolean);
  /** @param {HTMLElement} card */
  const matches = (card) =>
    scores.has(card.dataset.newsScore || "") &&
    (topics.size === allTopics.length || subjects(card).some((topic) => topics.has(topic)));
  const target = () => {
    const hash = location.hash.slice(1);
    let id;
    try {
      id = decodeURIComponent(hash);
    } catch {
      return null;
    }
    const card = document.getElementById(id)?.closest("[data-news-day]");
    return card instanceof HTMLElement && news.contains(card) ? card : null;
  };
  // A preview's "View All News" link opens the archive on the reader's choice, once
  // they have made one; the archive reads it as its own address.
  const carry = () => {
    const levels = allScores.filter((value) => scores.has(value)).join(",");
    for (const link of document.querySelectorAll("a[data-news-carry]")) {
      if (!(link instanceof HTMLAnchorElement)) {
        continue;
      }
      const url = new URL(link.href);
      if (levels === initial.join(",")) {
        url.searchParams.delete("news-s");
      } else {
        url.searchParams.set("news-s", levels || "none");
      }
      link.href = url.href;
    }
  };
  /** @param {"push" | "replace"} mode */
  const persist = (mode) => {
    if (preview) {
      carry();
      return;
    }
    const url = new URL(location.href);
    const levels = allScores.filter((value) => scores.has(value)).join(",");
    const selectedTopics = allTopics.filter((value) => topics.has(value)).join(",");
    if (levels === initial.join(",")) {
      url.searchParams.delete("news-s");
    } else {
      url.searchParams.set("news-s", levels || "none");
    }
    if (topics.size === allTopics.length) {
      url.searchParams.delete("news-topics");
    } else {
      url.searchParams.set("news-topics", selectedTopics || "none");
    }
    const named = target();
    if (named && !matches(named)) {
      url.hash = "";
    }
    if (url.href !== location.href) {
      if (mode === "push") {
        history.pushState(null, "", url);
      } else {
        history.replaceState(history.state, "", url);
      }
    }
  };
  // A preview's live count says what it shows, not what it carries for its filter.
  /** @param {number} shown */
  const previewCount = (shown) => {
    const levels = allScores.filter((value) => scores.has(value)).map((value) => `S${value}`);
    return shown
      ? `Showing ${shown} news item${shown === 1 ? "" : "s"} at ${levels.join(", ")}`
      : "No news matches these filters";
  };
  const apply = () => {
    const scored = cards.filter((card) => scores.has(card.dataset.newsScore || ""));
    for (const button of scoreButtons) {
      button.setAttribute(
        "aria-pressed",
        String(scores.has(button.getAttribute("data-news-score") || "")),
      );
    }
    for (const button of topicButtons) {
      const topic = button.getAttribute("data-news-topic") || "";
      button.setAttribute("aria-pressed", String(topics.has(topic)));
      const tally = button.querySelector("[data-news-tally]");
      if (tally) {
        tally.textContent = ` (${scored.filter((card) => subjects(card).includes(topic)).length})`;
      }
    }
    let shown = 0;
    for (const card of cards) {
      card.hidden = !matches(card) || (preview && shown >= limit);
      shown += Number(!card.hidden);
    }
    const count = controls.querySelector("[data-news-count]");
    if (count) {
      count.textContent = preview ? previewCount(shown) : `${shown} of ${cards.length} news items`;
    }
    const empty = controls.querySelector("[data-news-empty]");
    if (empty instanceof HTMLElement) {
      empty.hidden = shown !== 0;
    }
    document.dispatchEvent(new Event("news:filter"));
    controls.dispatchEvent(new CustomEvent("squares:filterschange", { bubbles: true }));
  };
  // A bookmarked item widens its facets, so the address never names a hidden card.
  const revealTarget = () => {
    const card = target();
    if (!card) {
      return;
    }
    scores.add(card.dataset.newsScore || "");
    const held = subjects(card);
    if (!held.some((topic) => topics.has(topic))) {
      if (held[0]) {
        topics.add(held[0]);
      } else {
        topics = new Set(allTopics);
      }
    }
  };
  /** @param {string} kind @param {string} value */
  const toggle = (kind, value) => {
    const chosen = kind === "data-news-score" ? scores : topics;
    if (chosen.has(value)) {
      chosen.delete(value);
    } else {
      chosen.add(value);
    }
    persist("push");
    apply();
  };
  controls.addEventListener("click", (event) => {
    const button = event.target instanceof Element ? event.target.closest("button") : null;
    if (!button) {
      return;
    }
    for (const kind of ["data-news-score", "data-news-topic"]) {
      const value = button.getAttribute(kind);
      if (value !== null) {
        toggle(kind, value);
        return;
      }
    }
    if (button.hasAttribute("data-site-filter-all")) {
      topics = new Set(allTopics);
    } else if (button.hasAttribute("data-news-reset")) {
      scores = new Set(initial);
      topics = new Set(allTopics);
    } else {
      return;
    }
    persist("push");
    apply();
  });
  const fromAddress = () => {
    restore();
    revealTarget();
    persist("replace");
    apply();
  };
  controls.hidden = false;
  if (preview) {
    apply();
    return;
  }
  fromAddress();
  window.addEventListener("popstate", fromAddress);
  window.addEventListener("hashchange", fromAddress);
})();
