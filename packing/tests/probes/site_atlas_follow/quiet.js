// Whether every move on the page has finished.
() => document.getAnimations().every((animation) => animation.playState === "finished");
