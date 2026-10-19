// The Visualize page's film starts when the page is visited.
//
// A browser starts a film unasked only when it is muted, so the film's markup mutes it,
// and it keeps its controls: a reader can pause it, seek, or turn it full screen. The
// markup does not carry `autoplay` itself. Markup cannot make that depend on what the
// reader asked of motion, and a film marked `preload="none"` that nothing starts fetches
// nothing. So the film is marked `data-autoplay`, and this starts it: it sets `autoplay`
// and plays, unless the reader asks for reduced motion, or the page is framed in a
// card's popover (`embed.js`), where looking at a preview should not start a download.
// A browser that will not start it rejects `play()`; the rejection is dropped and the
// film is paused, so it stays as it is for everyone else: its poster, with the play
// control. A film that cannot be fetched keeps its poster and controls too, as the
// browser leaves any film it cannot load.
(() => {
  // The picture is a keyboard-accessible play target; native controls remain below it.
  for (const video of document.querySelectorAll(".site-film-frame video")) {
    if (!(video instanceof HTMLVideoElement) || !video.parentElement) {
      continue;
    }
    const picture = document.createElement("div");
    picture.className = "site-film-picture";
    video.before(picture);
    picture.append(video);
    const play = document.createElement("button");
    play.type = "button";
    play.className = "site-film-play";
    play.setAttribute("aria-label", "Play video");
    const icon = document.createElement("span");
    icon.className = "site-film-play-icon";
    icon.setAttribute("aria-hidden", "true");
    play.append(icon);
    picture.append(play);
    const sync = () => {
      play.hidden = !video.paused && !video.ended;
    };
    play.addEventListener("click", () => {
      play.hidden = true;
      video.play().then(sync).catch(sync);
    });
    for (const event of ["play", "pause", "ended", "error"]) {
      video.addEventListener(event, sync);
    }
    sync();
  }
  const film = document.querySelector("video[data-autoplay]");
  if (!(film instanceof HTMLVideoElement)) {
    return;
  }
  const framed = document.documentElement.getAttribute("data-site-view") === "embed";
  if (framed || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }
  film.autoplay = true;
  film.play().catch(() => {
    // Refused: back to the poster and the play control.
    film.pause();
  });
})();
