// Clear any text selection, which a screenshot would otherwise draw over the stage.
() => {
  window.getSelection()?.removeAllRanges();
};
