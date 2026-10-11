// Native homepage player state and the shared main-heading spacing.
/** @param {{mockPlayback?: boolean, mediaEvent?: "pause" | "ended"}} [options] */
async (options) => {
  await document.fonts.ready;
  const film =
    document.querySelector(".site-homepage-film video") ??
    document.querySelector(".site-film-frame video");
  const article = document.querySelector(".site-page");
  if (!(film instanceof HTMLVideoElement) || !(article instanceof HTMLElement)) {
    throw new Error("The homepage has no native film player");
  }
  if (options?.mockPlayback && !film.hasAttribute("data-site-mock-plays")) {
    film.dataset.siteMockPlays = "0";
    film.dataset.siteMockPauses = "0";
    film.dataset.siteMockPaused = "true";
    film.dataset.siteMockEnded = "false";
    Object.defineProperties(film, {
      paused: { get: () => film.dataset.siteMockPaused !== "false" },
      ended: { get: () => film.dataset.siteMockEnded === "true" },
    });
    film.play = () => {
      film.dataset.siteMockPlays = String(Number(film.dataset.siteMockPlays) + 1);
      film.dataset.siteMockPaused = "false";
      film.dataset.siteMockEnded = "false";
      film.dispatchEvent(new Event("play"));
      return Promise.resolve();
    };
    film.pause = () => {
      film.dataset.siteMockPauses = String(Number(film.dataset.siteMockPauses) + 1);
      film.dataset.siteMockPaused = "true";
      film.dispatchEvent(new Event("pause"));
    };
    film.pause();
  }
  if (options?.mediaEvent === "pause") {
    film.pause();
  } else if (options?.mediaEvent === "ended") {
    film.dataset.siteMockEnded = "true";
    film.dispatchEvent(new Event("ended"));
  }
  const overlay = document.querySelector(".site-film-play");
  const box = film.getBoundingClientRect();
  const frame = article.getBoundingClientRect();
  const rem = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
  const measure = document.createElement("span");
  measure.style.marginBlockStart = "var(--site-title-space-above)";
  measure.style.marginBlockEnd = "var(--site-title-space-below)";
  article.append(measure);
  const spacing = getComputedStyle(measure);
  const titleAbove = Number.parseFloat(spacing.marginBlockStart);
  const titleBelow = Number.parseFloat(spacing.marginBlockEnd);
  measure.remove();
  if (!(titleAbove > 0 && titleBelow > 0)) {
    throw new Error("The shared title spacing tokens must resolve");
  }
  return {
    controls: film.controls,
    overlay_visible: overlay instanceof HTMLButtonElement && !overlay.hidden,
    overlay_label: overlay?.getAttribute("aria-label"),
    mock_play_calls: Number(film.dataset.siteMockPlays ?? 0),
    mock_pause_calls: Number(film.dataset.siteMockPauses ?? 0),
    inline: film.playsInline,
    preload: film.preload,
    autoplay: film.autoplay,
    marked_autoplay: film.hasAttribute("data-autoplay"),
    paused: film.paused,
    ready: film.readyState,
    time: film.currentTime,
    source: film.querySelector("source")?.getAttribute("src"),
    poster: film.getAttribute("poster"),
    label: film.getAttribute("aria-label"),
    codec: film.canPlayType('video/mp4; codecs="avc1.640028"'),
    width: box.width,
    height: box.height,
    left: box.left,
    right: box.right,
    center_offset: (box.left + box.right - frame.left - frame.right) / 2,
    max_width: 52 * rem,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    headings: [...article.querySelectorAll("h1.site-title, h2.site-title")].map((heading) => ({
      id: heading.id,
      above: Number.parseFloat(getComputedStyle(heading).marginBlockStart),
      below: Number.parseFloat(getComputedStyle(heading).marginBlockEnd),
    })),
    title_above: titleAbove,
    title_below: titleBelow,
  };
};
