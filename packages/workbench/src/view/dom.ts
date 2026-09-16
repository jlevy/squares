const SVG_NS = "http://www.w3.org/2000/svg";

/** Required template bindings fail at startup, where a missing element is actionable. */
export function requireHtml(document: Document, id: string): HTMLElement {
  const node = document.getElementById(id);
  if (!(node instanceof HTMLElement)) {
    throw new Error(`workbench template is missing HTML element ${id}`);
  }
  return node;
}

export function requireSvg(document: Document, id: string): SVGElement {
  const node = document.getElementById(id);
  if (!(node instanceof SVGElement)) {
    throw new Error(`workbench template is missing SVG element ${id}`);
  }
  return node;
}

export function createDom(document: Document) {
  function input(id: string): HTMLInputElement {
    const node = requireHtml(document, id);
    if (!(node instanceof HTMLInputElement)) {
      throw new Error(`workbench template needs an input at ${id}`);
    }
    return node;
  }

  function select(id: string): HTMLSelectElement {
    const node = requireHtml(document, id);
    if (!(node instanceof HTMLSelectElement)) {
      throw new Error(`workbench template needs a select at ${id}`);
    }
    return node;
  }
  function el<Tag extends keyof SVGElementTagNameMap>(
    tag: Tag,
    attrs: Readonly<Record<string, string | number>> = {},
  ): SVGElementTagNameMap[Tag] {
    const node = document.createElementNS(SVG_NS, tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (typeof value === "number" && !Number.isFinite(value)) {
        throw new RangeError(`nonfinite SVG attribute ${key}`);
      }
      node.setAttribute(key, String(value));
    }
    return node;
  }

  function text(tag: string, className?: string, content?: string): HTMLElement {
    const node = document.createElement(tag);
    if (className !== undefined) {
      node.className = className;
    }
    if (content !== undefined) {
      node.textContent = content;
    }
    return node;
  }
  return {
    el,
    text,
    input,
    select,
    html: (id: string) => requireHtml(document, id),
    svg: (id: string) => requireSvg(document, id),
  };
}
