// Where the stage sits against the window it has to fit inside.
() => {
  const s = document.getElementById('stage').getBoundingClientRect();
  return {top: s.top, bottom: s.bottom, h: window.innerHeight};
}
