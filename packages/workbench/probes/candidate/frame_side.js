// The container side the record states for one frame. Takes {n}.
/** @param {{n: number}} o */
(o) => {
  const data = document.getElementById("atlas-data")?.textContent;
  if (data == null) {
    throw new Error("probe requires #atlas-data text");
  }
  return JSON.parse(data).frames[String(o.n)].side;
};
