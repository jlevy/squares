// Play the step and sample it every 60 ms, collecting [t, the bar's hand, the frame's own
// summed overlap] until the run stops. The overlap is measured from the poses of every
// frame, so it moves while the bar deliberately does not.
() => {
  window.__samples = [];
  const api = window.atlasTransitions;
  api.seek(0);
  api.play();
  const id = setInterval(() => {
    const st = api.state();
    window.__samples.push([st.t, api.gapBar().x, api.colour().overlap]);
    if (!st.playing) {
      clearInterval(id);
    }
  }, 60);
};
