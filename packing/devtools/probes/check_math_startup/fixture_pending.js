// The startup fixture page's head script: the page starts with its math pending, as the
// publication's bootstrap marks it.
() => {
  document.documentElement.dataset.kpressMathPending = "true";
};
