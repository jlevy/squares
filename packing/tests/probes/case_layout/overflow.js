// Preserve the original full-page overflow oracle and count real style reads.
/** @param {{mode: "install" | "read" | "restore"}} options */
(options) => {
  const scope = /** @type {typeof globalThis & {
    caseLayoutStyleReads?: {native: typeof getComputedStyle, count: number, fixture: HTMLElement,
      overflow: string, priority: string}
  }} */ (globalThis);
  if (options.mode === "install") {
    if (scope.caseLayoutStyleReads) {
      throw new Error("Case layout style counter is already installed");
    }
    const fixture = document.createElement("div");
    fixture.className = "case-overflow-fixture root";
    fixture.style.cssText = "position:absolute;left:-20px;top:0;width:10px;overflow:visible";
    const overflow = document.body.style.getPropertyValue("overflow-x");
    const priority = document.body.style.getPropertyPriority("overflow-x");
    document.body.style.setProperty("overflow-x", "visible", "important");
    for (const value of ["visible", "auto", "scroll", "hidden", "clip"]) {
      const host = document.createElement("div");
      host.className = `case-overflow-fixture host-${value}`;
      host.style.cssText = `width:10px;overflow:${value}`;
      const child = document.createElement("div");
      child.className = `case-overflow-fixture child-${value}`;
      child.style.width = "10px";
      host.append(child);
      fixture.append(host);
    }
    const nested = document.createElement("div");
    nested.className = "case-overflow-fixture nested-hidden";
    nested.style.cssText = "width:10px;overflow:hidden";
    const intermediary = document.createElement("div");
    intermediary.className = "case-overflow-fixture intermediary-visible";
    intermediary.style.cssText = "width:10px;overflow:visible";
    const grandchild = document.createElement("div");
    grandchild.className = "case-overflow-fixture nested-grandchild";
    grandchild.style.width = "10px";
    intermediary.append(grandchild);
    nested.append(intermediary);
    fixture.append(nested);
    const sibling = document.createElement("div");
    sibling.className = "case-overflow-fixture outside-sibling";
    sibling.style.width = "10px";
    fixture.append(sibling);
    const threshold = document.createElement("div");
    threshold.className = "case-overflow-fixture threshold";
    threshold.style.cssText = "position:fixed;left:-1px;width:1px";
    fixture.append(threshold);
    for (let i = 0; i < 35; i += 1) {
      const extra = document.createElement("div");
      extra.className = `case-overflow-fixture extra-${i}`;
      extra.style.width = "10px";
      fixture.append(extra);
    }
    document.body.prepend(fixture);
    const state = { native: getComputedStyle, count: 0, fixture, overflow, priority };
    scope.caseLayoutStyleReads = state;
    globalThis.getComputedStyle = (element, pseudo) => {
      state.count += 1;
      return state.native.call(globalThis, element, pseudo);
    };
    return null;
  }
  const state = scope.caseLayoutStyleReads;
  if (!state) {
    throw new Error("Case layout style counter was not installed");
  }
  if (options.mode === "restore") {
    globalThis.getComputedStyle = state.native;
    state.fixture.remove();
    if (state.overflow) {
      document.body.style.setProperty("overflow-x", state.overflow, state.priority);
    } else {
      document.body.style.removeProperty("overflow-x");
    }
    delete scope.caseLayoutStyleReads;
    return null;
  }
  const actualStyleReads = state.count;
  const overflowing = [...document.querySelectorAll("body *")]
    .filter((node) => {
      for (let ancestor = node.parentElement; ancestor; ancestor = ancestor.parentElement) {
        if (["auto", "scroll", "hidden", "clip"].includes(getComputedStyle(ancestor).overflowX)) {
          return false;
        }
      }
      return true;
    })
    .map((node) => ({
      element: node.tagName,
      classes: node.getAttribute("class"),
      text: node.textContent?.slice(0, 80),
      left: node.getBoundingClientRect().left,
      right: node.getBoundingClientRect().right,
    }))
    .filter((node) => node.right > innerWidth + 1 || node.left < -1)
    .slice(0, 30);
  return { overflowing, actualStyleReads, legacyStyleReads: state.count - actualStyleReads };
};
