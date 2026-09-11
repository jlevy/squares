// Take the focus off whatever holds it.
() => {
  if (document.activeElement) {
    document.activeElement.blur();
  }
};
