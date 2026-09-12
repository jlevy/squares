// Each readout that changes at runtime, as [its id, whether it is a readout, its width, its
// overflow, whether it takes a line of its own]. o.ids is the list to ask about.
(o) =>
  o.ids.map((id) => {
    const e = document.getElementById(id);
    const s = getComputedStyle(e);
    return [
      id,
      e.classList.contains("readout"),
      s.width,
      s.overflow,
      e.classList.contains("readout-line"),
    ];
  });
