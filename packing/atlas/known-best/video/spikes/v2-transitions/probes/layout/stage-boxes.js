// The boxes the two modes must lay out identically, and whether the position bar is gone.
() => {
  const r = (id) => {
    const b = document.getElementById(id).getBoundingClientRect();
    return [b.x, b.y, b.width, b.height];
  };
  return {stage: r('stage'), facts: r('facts'), svg: r('packing-svg'),
          progress: document.getElementById('progress') === null};
}
