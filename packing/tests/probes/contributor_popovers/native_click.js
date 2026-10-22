/** @param {string} modifier */
(modifier) => {
  const link = document.querySelector("#profile-link");
  if (!(link instanceof HTMLAnchorElement)) {
    throw new Error("Missing contributor link");
  }
  const click = new MouseEvent("click", { bubbles: true, cancelable: true, [modifier]: true });
  // Read the enhancement's disposition before suppressing the synthetic navigation.
  let prevented = false;
  document.addEventListener(
    "click",
    (event) => {
      prevented = event.defaultPrevented;
      event.preventDefault();
    },
    { once: true },
  );
  link.dispatchEvent(click);
  return prevented;
};
