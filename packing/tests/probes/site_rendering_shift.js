// Deliberate early layout shift proves the observer starts before page load.
() => {
  document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
      const gap = document.createElement("div");
      gap.style.height = "500px";
      document.body.prepend(gap);
    }, 120);
  });
};
