// Run as an init script, before the page's own scripts: keeps every Content-Security-Policy
// violation the document reports, where `policy/violations` reads them after load. A listener
// added after load would miss a violation raised while the page was parsed.
() => {
  /** @type {{ directive: string, blocked: string, source: string }[]} */
  const seen = [];
  document.addEventListener(
    "securitypolicyviolation",
    (event) => {
      seen.push({
        directive: event.effectiveDirective,
        blocked: event.blockedURI,
        source: event.sourceFile,
      });
    },
    true,
  );
  Object.defineProperty(window, "squaresPolicyViolations", { value: seen });
};
