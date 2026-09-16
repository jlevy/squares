// What the page's own data says about one size. o.n is the size.
/** @param {{n: number}} o */
(o) => {
  const data = document.getElementById("atlas-data")?.textContent;
  if (data == null) {
    throw new Error("probe requires #atlas-data text");
  }
  return JSON.parse(data).facts[String(o.n)];
};
