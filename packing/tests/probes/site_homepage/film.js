// Native homepage player state and the modest main-heading spacing increment.
async () => {
  await document.fonts.ready;
  const film = document.querySelector(".site-homepage-film video");
  const article = document.querySelector(".site-page");
  if (!(film instanceof HTMLVideoElement) || !(article instanceof HTMLElement)) {
    throw new Error("The homepage has no native film player");
  }
  const box = film.getBoundingClientRect();
  const frame = article.getBoundingClientRect();
  const rem = Number.parseFloat(getComputedStyle(document.documentElement).fontSize);
  const measure = document.createElement("span");
  measure.style.marginBlockStart = "var(--paper-section-space)";
  article.append(measure);
  const sectionSpace = Number.parseFloat(getComputedStyle(measure).marginBlockStart);
  measure.remove();
  return {
    controls: film.controls,
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
      before: heading.tagName === "H1" ? 2 * rem : sectionSpace,
    })),
    extra_space: 0.5 * rem,
    legend_above: Number.parseFloat(
      getComputedStyle(article.querySelector(".site-rung-legend-heading") ?? article)
        .marginBlockStart,
    ),
  };
};
