// Every Content-Security-Policy violation `policy/record-violations` kept, or null when the
// recorder never ran, so a check cannot read a missing recorder as a clean page.
() => {
  const seen = Reflect.get(window, "squaresPolicyViolations");
  return Array.isArray(seen) ? seen : null;
};
