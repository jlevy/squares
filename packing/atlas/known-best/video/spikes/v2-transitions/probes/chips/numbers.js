// The size each quick-pick chip stands for, in the order they are drawn.
() => Array.from(document.querySelectorAll("#step-chips button")).map((b) => Number(b.dataset.n));
