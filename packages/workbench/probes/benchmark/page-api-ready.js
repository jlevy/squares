// Whether the page has installed its workbench API. A function, not an expression string:
// under the page's Content-Security-Policy, which has no 'unsafe-eval', Playwright refuses to
// poll an expression-string predicate that is false on its first check.
() => window.atlasTransitions !== undefined;
