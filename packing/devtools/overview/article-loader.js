// Case, result and contributor overlays read the canonical article through one boundary.
// The cache owns pristine, inert markup; every consumer gets a new, ID-scoped clone.
(() => {
  /** @type {Map<string, Promise<SiteLoadedArticle>>} */
  const articles = new Map();
  /** @type {Map<string, Promise<void>>} */
  const mathStyles = new Map();
  /** @type {WeakMap<HTMLElement, HTMLElement>} */
  const origins = new WeakMap();
  /** @type {((article: HTMLElement) => void)[]} what a controller adds to every clone */
  const preparers = [];
  let serial = 0;
  let generation = 0;

  /** @param {string} address */
  const sameSite = (address) => {
    const url = new URL(address, document.baseURI);
    if (!/^https?:$/.test(url.protocol) || url.origin !== new URL(document.baseURI).origin) {
      throw new Error("The article is outside this site");
    }
    url.hash = "";
    return url;
  };

  /** @param {DocumentFragment} parsed @param {string} base */
  const loadMathStyles = async (parsed, base) => {
    const responseURL = sameSite(base);
    const assetRoot = new URL("../assets/css/", responseURL);
    for (const declared of parsed.querySelectorAll("link[data-site-math-styles]")) {
      const href = declared.getAttribute("href");
      if (!href) {
        throw new Error("The prepared mathematics stylesheet has no address");
      }
      const url = sameSite(new URL(href, responseURL).href);
      if (!url.pathname.startsWith(assetRoot.pathname) || !url.pathname.endsWith(".css")) {
        throw new Error("The prepared mathematics stylesheet is outside this site");
      }
      let pending = mathStyles.get(url.href);
      if (pending === undefined) {
        const existing = Array.from(document.querySelectorAll("link[data-site-math-styles]")).find(
          (link) => new URL(link.getAttribute("href") || "", document.baseURI).href === url.href,
        );
        const link =
          existing instanceof HTMLLinkElement ? existing : document.createElement("link");
        pending = link.sheet
          ? Promise.resolve()
          : new Promise((resolve, reject) => {
              link.addEventListener("load", () => resolve(), { once: true });
              link.addEventListener(
                "error",
                () => {
                  link.remove();
                  reject(new Error("The prepared mathematics stylesheet could not load"));
                },
                { once: true },
              );
              if (!existing) {
                link.setAttribute("rel", "stylesheet");
                link.setAttribute("href", url.href);
                link.setAttribute("data-site-math-styles", "");
                document.head.append(link);
              }
            });
        mathStyles.set(url.href, pending);
        void pending.catch(() => mathStyles.delete(url.href));
      }
      await pending;
    }
  };

  /** Attributes whose value is an address the clone follows or loads. */
  const ADDRESSES = ["href", "src", "xlink:href", "action", "formaction"];

  /**
   * Leave a parsed article nothing that runs once it is cloned into the live document:
   * no script, event handler attribute, `srcdoc` or `javascript:` address. Relative
   * `href` and `src` values are resolved against the response. The pages are this site's
   * own, generated with their text escaped, so this is defence in depth over them rather
   * than a sanitizer for foreign markup.
   * @param {HTMLElement} article @param {string} responseUrl
   */
  const inert = (article, responseUrl) => {
    for (const script of article.querySelectorAll("script")) {
      script.remove();
    }
    for (const node of [article, ...article.querySelectorAll("*")]) {
      for (const { name } of Array.from(node.attributes)) {
        const lower = name.toLowerCase();
        if (lower.startsWith("on") || lower === "srcdoc") {
          node.removeAttribute(name);
          continue;
        }
        const value = ADDRESSES.includes(lower) ? node.getAttribute(name)?.trim() : undefined;
        if (value === undefined || value.startsWith("#")) {
          continue;
        }
        const address = new URL(value, responseUrl);
        if (address.protocol === "javascript:") {
          node.removeAttribute(name);
        } else if (lower === "href" || lower === "src") {
          node.setAttribute(name, address.href);
        }
      }
    }
  };

  /** @param {string} url @param {string} selector @returns {Promise<SiteLoadedArticle>} */
  const fetchArticle = async (url, selector) => {
    const response = await fetch(url, { credentials: "same-origin", mode: "same-origin" });
    if (!response.ok) {
      throw new Error(`${url}: ${response.status}`);
    }
    const responseUrl = sameSite(response.url || url).href;
    const parsed = document.createElement("template");
    parsed.innerHTML = await response.text();
    const article = parsed.content.querySelector(selector);
    if (!(article instanceof HTMLElement)) {
      throw new Error(`${url} holds no ${selector} article`);
    }
    inert(article, responseUrl);
    await loadMathStyles(parsed.content, responseUrl);
    article.remove();
    return { article, responseUrl };
  };

  /** Scope headings, SVG definitions and their references to this article instance.
   * @param {HTMLElement} article @param {string} responseUrl
   */
  const scopeIds = (article, responseUrl) => {
    const prefix = `site-article-${++serial}-`;
    const nodes = [article, ...article.querySelectorAll("*")];
    const ids = new Map();
    for (const node of nodes) {
      if (node.id) {
        ids.set(node.id, prefix + node.id);
        node.id = prefix + node.id;
      }
    }
    const references = [
      "aria-labelledby",
      "aria-describedby",
      "aria-controls",
      "aria-owns",
      "aria-flowto",
      "aria-details",
      "aria-errormessage",
      "aria-activedescendant",
      "for",
      "headers",
      "list",
      "form",
    ];
    for (const node of nodes) {
      for (const name of references) {
        const value = node.getAttribute(name);
        if (value !== null) {
          node.setAttribute(
            name,
            value
              .split(/\s+/)
              .map((id) => ids.get(id) || id)
              .join(" "),
          );
        }
      }
      for (const attribute of Array.from(node.attributes)) {
        if (
          (attribute.name === "href" || attribute.name === "xlink:href") &&
          attribute.value.startsWith("#")
        ) {
          const id = attribute.value.slice(1);
          node.setAttribute(
            attribute.name,
            ids.has(id) ? `#${ids.get(id)}` : new URL(attribute.value, responseUrl).href,
          );
        } else if (attribute.value.includes("url(#")) {
          node.setAttribute(
            attribute.name,
            attribute.value.replace(/url\(#([^)]*)\)/g, (match, id) =>
              ids.has(id) ? `url(#${ids.get(id)})` : match,
            ),
          );
        }
      }
    }
  };

  /** @param {string} address @param {string} selector @returns {Promise<SiteLoadedArticle>} */
  const loadArticle = async (address, selector) => {
    const url = sameSite(address).href;
    const key = `${url}\n${selector}`;
    let pending = articles.get(key);
    if (pending === undefined) {
      pending = fetchArticle(url, selector);
      articles.set(key, pending);
      void pending.catch(() => articles.delete(key));
    }
    const held = await pending;
    const article = /** @type {HTMLElement} */ (held.article.cloneNode(true));
    scopeIds(article, held.responseUrl);
    for (const prepare of preparers) {
      prepare(article);
    }
    return { article, responseUrl: held.responseUrl };
  };

  /** @param {HTMLElement} opener @returns {HTMLElement} */
  const returnFocus = (opener) => {
    const popover = opener.closest(".site-popover[popover]");
    return popover instanceof HTMLElement ? origins.get(popover) || opener : opener;
  };

  /** @param {MouseEvent} event @returns {Element | null} */
  const clickTarget = (event) =>
    event.defaultPrevented ||
    event.button !== 0 ||
    event.metaKey ||
    event.ctrlKey ||
    event.shiftKey ||
    event.altKey ||
    !(event.target instanceof Element)
      ? null
      : event.target;

  globalThis.siteArticles = {
    loadArticle,
    prepare: (step) => {
      preparers.push(step);
    },
    clickTarget,
    returnFocus,
    setReturnFocus: (popover, opener) => origins.set(popover, returnFocus(opener)),
    beginRequest: () => ++generation,
    isCurrent: (request) => request === generation,
    cancelRequests: () => {
      generation += 1;
    },
  };
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      globalThis.siteArticles?.cancelRequests();
    }
  });
})();
