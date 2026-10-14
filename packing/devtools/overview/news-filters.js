// Facets enhance the complete archive; without scripts no article is filtered out.
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
  let scores = new Set(["4", "5"]);
  let topics = new Set(allTopics);
  /** @param {string} name @param {string[]} allowed @param {string[]} fallback */
  const read = (name, allowed, fallback) => {
    const value = new URL(location.href).searchParams.get(name);
    return new Set(
      value === null ? fallback : value.split(",").filter((item) => allowed.includes(item)),
    );
  };
  const restore = () => {
    scores = read("news-s", allScores, ["4", "5"]);
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
  /** @param {"push" | "replace"} mode */
  const persist = (mode) => {
    const url = new URL(location.href);
    const levels = allScores.filter((value) => scores.has(value)).join(",");
    const selectedTopics = allTopics.filter((value) => topics.has(value)).join(",");
    if (levels === "4,5") {
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
  const apply = () => {
    for (const button of scoreButtons) {
      button.setAttribute(
        "aria-pressed",
        String(scores.has(button.getAttribute("data-news-score") || "")),
      );
    }
    for (const button of topicButtons) {
      button.setAttribute(
        "aria-pressed",
        String(topics.has(button.getAttribute("data-news-topic") || "")),
      );
    }
    let shown = 0;
    for (const card of cards) {
      card.hidden = !matches(card);
      shown += Number(!card.hidden);
    }
    const count = controls.querySelector("[data-news-count]");
    if (count) {
      count.textContent = `${shown} of ${cards.length} news items`;
    }
    const empty = controls.querySelector("[data-news-empty]");
    if (empty instanceof HTMLElement) {
      empty.hidden = shown !== 0;
    }
    document.dispatchEvent(new Event("news:filter"));
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
    if (button.hasAttribute("data-news-reset")) {
      scores = new Set(["4", "5"]);
      topics = new Set(allTopics);
    } else if (button.getAttribute("data-news-all") === "scores") {
      scores = new Set(allScores);
    } else if (button.getAttribute("data-news-all") === "topics") {
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
  fromAddress();
  window.addEventListener("popstate", fromAddress);
  window.addEventListener("hashchange", fromAddress);
})();
