// Every identity the pool holds, in the order its elements sit in the document.
() =>
  Array.from(document.querySelectorAll("#squares g[data-identity]")).map((g) =>
    Number(g.dataset.identity),
  );
