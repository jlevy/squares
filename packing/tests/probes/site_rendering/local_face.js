// Whether a face declared from these `local()` sources resolves on this machine. Chromium
// rejects the load when none of them is installed, so a metric-adjusted alias in
// `paper-type.css` that names them would have nothing to stand in with.
/** @param {string} source */
async (source) => {
  try {
    await new FontFace("Local Face Probe", source).load();
    return true;
  } catch {
    return false;
  }
};
