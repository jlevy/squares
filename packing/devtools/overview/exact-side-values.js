/** Browse a small index; fetch metadata and exact integer strings only on demand. */
(() => {
  const root = document.getElementById("exact-browser");
  if (!root) {
    return;
  }
  const entryBatch = 25;
  const coefficientBatch = 12;
  const fetchTimeoutMs = 15_000;
  /** @param {string} id @returns {HTMLElement} */
  const element = (id) => {
    const node = document.getElementById(id);
    if (!node) {
      throw new Error(`Missing catalogue element: ${id}`);
    }
    return node;
  };
  /** @param {string} id @returns {HTMLButtonElement} */
  const button = (id) => /** @type {HTMLButtonElement} */ (element(id));
  const search = /** @type {HTMLInputElement} */ (element("entry-search"));
  const section = /** @type {HTMLSelectElement} */ (element("entry-section"));
  const kind = /** @type {HTMLSelectElement} */ (element("entry-kind"));
  const status = /** @type {HTMLSelectElement} */ (element("entry-status"));
  const list = element("entry-list");
  const indexMessage = element("index-message");
  const detailMessage = element("detail-message");
  const coefficientMessage = element("coefficient-message");
  /** @type {ExactSideEntry[]} */
  let entries = [];
  /** @type {ExactSideEntry | null} */
  let selected = null;
  /** @type {ExactSideCoefficients | null} */
  let coefficients = null;
  let entryPage = 0;
  let coefficientPage = 0;
  let selectionVersion = 0;
  let coefficientVersion = 0;
  let indexVersion = 0;
  /** @type {AbortController | null} */
  let metadataAbort = null;
  /** @type {AbortController | null} */
  let coefficientAbort = null;

  /** @param {unknown} value @returns {value is Record<string, unknown>} */
  const object = (value) => typeof value === "object" && value !== null && !Array.isArray(value);
  /** @param {string} value @returns {string} */
  const safeUrl = (value) => {
    const url = new URL(value, document.baseURI);
    if (url.protocol !== "https:" && url.protocol !== "http:") {
      throw new Error("Catalogue links must use HTTP or HTTPS.");
    }
    return value;
  };
  /** @param {string} url @param {AbortSignal | undefined} signal @returns {Promise<unknown>} */
  const fetchJson = async (url, signal) => {
    const deadline = AbortSignal.timeout(fetchTimeoutMs);
    const response = await fetch(safeUrl(url), {
      signal: signal ? AbortSignal.any([signal, deadline]) : deadline,
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} while loading ${url}`);
    }
    return /** @type {unknown} */ (await response.json());
  };
  /** @param {unknown} error @returns {string} */
  const errorText = (error) => (error instanceof Error ? error.message : String(error));
  /** @param {unknown} value @returns {ExactSideEntry[]} */
  const readIndex = (value) => {
    if (!object(value) || value.schema_version !== 1 || !Array.isArray(value.entries)) {
      throw new Error("Unsupported catalogue index format.");
    }
    const identities = new Set();
    for (const row of value.entries) {
      if (
        !object(row) ||
        typeof row.id !== "string" ||
        identities.has(row.id) ||
        !Number.isSafeInteger(row.n) ||
        (row.section !== "current" && row.section !== "historical") ||
        (row.kind !== "polynomial" && row.kind !== "numeric") ||
        typeof row.title !== "string" ||
        typeof row.component !== "string" ||
        typeof row.status !== "string" ||
        typeof row.metadata_url !== "string" ||
        (row.coefficients_url !== null && typeof row.coefficients_url !== "string")
      ) {
        throw new Error("Malformed or duplicate catalogue entry.");
      }
      identities.add(row.id);
    }
    return /** @type {ExactSideEntry[]} */ (value.entries);
  };
  /** Validate the selected payload without converting any coefficient string.
   * @param {unknown} value @param {ExactSideEntry} row
   * @returns {value is ExactSideCoefficients}
   */
  const coefficientPayload = (value, row) =>
    object(value) &&
    value.schema_version === 1 &&
    value.id === row.id &&
    value.order === "descending" &&
    Array.isArray(value.coefficients) &&
    value.coefficients.length > 0 &&
    value.coefficients.every(
      (coefficient) => typeof coefficient === "string" && /^[+-]?\d+$/.test(coefficient),
    ) &&
    (row.degree === null || value.coefficients.length === row.degree + 1);
  /** @param {ExactSideEntry} row @returns {boolean} */
  const matches = (row) => {
    if (
      (section.value !== "all" && row.section !== section.value) ||
      (kind.value !== "all" && row.kind !== kind.value) ||
      (status.value !== "all" && row.status !== status.value)
    ) {
      return false;
    }
    const text = [row.title, row.n, row.component, row.status, row.degree, row.search_text ?? ""]
      .join(" ")
      .toLowerCase();
    return search.value
      .toLowerCase()
      .trim()
      .split(/\s+/)
      .every((token) => {
        const exactN = /^n:(\d+)$/.exec(token);
        return exactN ? String(row.n) === exactN[1] : text.includes(token);
      });
  };
  /** Rebuild only one small batch; a selection remains stable when filters change. */
  const renderEntries = () => {
    const filtered = entries.filter(matches);
    const pages = Math.ceil(filtered.length / entryBatch);
    entryPage = Math.max(0, Math.min(entryPage, pages - 1));
    list.replaceChildren();
    for (const row of filtered.slice(entryPage * entryBatch, (entryPage + 1) * entryBatch)) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.className = "entry-link";
      link.href = `#${encodeURIComponent(row.legacy_anchor || row.id)}`;
      if (selected?.id === row.id) {
        link.setAttribute("aria-current", "true");
      }
      const title = document.createElement("strong");
      title.textContent = row.title;
      const summary = document.createElement("span");
      summary.className = "entry-summary";
      summary.textContent = `${row.section === "historical" ? "Historical" : "Current"} · ${row.kind === "numeric" ? "Numeric" : `Polynomial, degree ${row.degree}`} · ${row.status}`;
      link.append(title, summary);
      link.addEventListener("click", (event) => {
        event.preventDefault();
        if (window.location.hash !== link.hash) {
          history.pushState(null, "", link.hash);
        }
        selectEntry(row, true);
      });
      item.append(link);
      list.append(item);
    }
    const current = entries.filter((row) => row.section === "current").length;
    indexMessage.textContent = filtered.length
      ? `${filtered.length} matching entries · ${current} current, ${entries.length - current} historical in the catalogue.`
      : "No entries match these filters. Clear filters or try another case number, source or status.";
    element("entry-page").textContent = pages ? `Page ${entryPage + 1} of ${pages}` : "";
    button("previous-entries").disabled = entryPage === 0 || pages === 0;
    button("next-entries").disabled = entryPage + 1 >= pages;
  };

  /** Preserve every original metadata field and attribution as literal text. @param {unknown} value @param {string} key @returns {Node} */
  const metadataNode = (value, key) => {
    if (Array.isArray(value)) {
      const items = document.createElement("ul");
      if (!value.length) {
        items.textContent = "[]";
      }
      for (const child of value) {
        const item = document.createElement("li");
        item.append(metadataNode(child, key));
        items.append(item);
      }
      return items;
    }
    if (object(value)) {
      const fields = document.createElement("dl");
      fields.className = "metadata-fields";
      for (const [name, child] of Object.entries(value)) {
        const field = document.createElement("div");
        field.className = "metadata-field";
        const term = document.createElement("dt");
        term.textContent = name.replaceAll("_", " ");
        const description = document.createElement("dd");
        description.append(metadataNode(child, name));
        field.append(term, description);
        fields.append(field);
      }
      return fields;
    }
    const text = value === null ? "null (not recorded)" : String(value);
    if (typeof value === "string" && (key === "url" || key.endsWith("_url"))) {
      try {
        const link = document.createElement("a");
        link.href = safeUrl(value);
        link.textContent = value;
        return link;
      } catch {
        // Preserve an unsupported source URL as text, without making an executable link.
      }
    }
    const span = document.createElement("span");
    span.textContent = text;
    return span;
  };

  /** A native equation describes the selected vector without loading a math runtime.
   * @param {ExactSideEntry} row @param {string[] | null} vector
   */
  const renderEquation = (row, vector = null) => {
    const host = element("entry-equation");
    host.replaceChildren();
    host.hidden = row.kind !== "polynomial" || row.degree === null;
    if (host.hidden) {
      return;
    }
    /** @param {string} tag @param {string} [text] */
    const mathNode = (tag, text) => {
      const node = document.createElementNS("http://www.w3.org/1998/Math/MathML", tag);
      if (text !== undefined) {
        node.textContent = text;
      }
      return node;
    };
    const math = mathNode("math");
    math.setAttribute(
      "aria-label",
      `${row.section === "historical" ? "Historical" : "Current"} polynomial ${row.component}, degree ${row.degree}`,
    );
    const formula = mathNode("mrow");
    const name = mathNode("msub");
    name.append(
      mathNode("mi", row.section === "historical" ? "H" : "P"),
      mathNode(
        "mn",
        row.section === "historical" ? row.component.replace(/^H_/, "") : String(row.n),
      ),
    );
    formula.append(
      name,
      mathNode("mo", "("),
      mathNode("mi", "s"),
      mathNode("mo", ")"),
      mathNode("mo", "="),
    );
    if (vector && vector.length <= 9) {
      let first = true;
      vector.forEach((coefficient, index) => {
        if (/^[+-]?0+$/.test(coefficient)) {
          return;
        }
        const negative = coefficient.startsWith("-");
        if (!first || negative) {
          formula.append(mathNode("mo", negative ? "−" : "+"));
        }
        const magnitude = coefficient.replace(/^[+-]/, "");
        const power = vector.length - index - 1;
        if (magnitude !== "1" || power === 0) {
          formula.append(mathNode("mn", magnitude));
        }
        if (power > 0) {
          const factor = power === 1 ? mathNode("mi", "s") : mathNode("msup");
          if (power > 1) {
            factor.append(mathNode("mi", "s"), mathNode("mn", String(power)));
          }
          formula.append(factor);
        }
        first = false;
      });
    } else {
      const sum = mathNode("munderover");
      const lower = mathNode("mrow");
      lower.append(mathNode("mi", "k"), mathNode("mo", "="), mathNode("mn", "0"));
      sum.append(mathNode("mo", "∑"), lower, mathNode("mn", String(row.degree)));
      const coefficient = mathNode("msub");
      coefficient.append(mathNode("mi", "a"), mathNode("mi", "k"));
      const power = mathNode("msup");
      power.append(mathNode("mi", "s"), mathNode("mi", "k"));
      formula.append(sum, coefficient, power);
    }
    formula.append(mathNode("mo", "="), mathNode("mn", "0"));
    math.append(formula);
    host.append(math);
  };

  /** @param {ExactSideEntry} row @param {number} version */
  const loadMetadata = async (row, version) => {
    const abort = new AbortController();
    metadataAbort = abort;
    detailMessage.textContent = "Loading recorded metadata…";
    button("retry-metadata").hidden = true;
    try {
      const value = await fetchJson(row.metadata_url, abort.signal);
      if (version !== selectionVersion) {
        return;
      }
      if (
        !object(value) ||
        value.schema_version !== 1 ||
        value.id !== row.id ||
        !object(value.record) ||
        typeof value.claim !== "string"
      ) {
        throw new Error("Metadata does not match the selected entry.");
      }
      element("entry-claim").textContent = value.claim;
      renderEquation(row);
      element("metadata").replaceChildren(metadataNode(value.record, "record"));
      element("detail-content").hidden = false;
      element("coefficient-section").hidden = !row.coefficients_url;
      detailMessage.textContent = `${row.section === "historical" ? "Historical source record" : "Current record"} · ${row.kind} · ${row.status}`;
    } catch (error) {
      if (version === selectionVersion && !abort.signal.aborted) {
        detailMessage.textContent = `Could not load this entry: ${errorText(error)}. Retry or use the complete archives.`;
        button("retry-metadata").hidden = false;
      }
    }
  };
  /** @param {ExactSideEntry} row @param {boolean} focus */
  const selectEntry = (row, focus) => {
    metadataAbort?.abort();
    coefficientAbort?.abort();
    selectionVersion += 1;
    coefficientVersion += 1;
    selected = row;
    coefficients = null;
    coefficientPage = 0;
    element("detail-title").textContent = row.title;
    element("entry-equation").hidden = true;
    const report = /** @type {HTMLAnchorElement} */ (element("entry-report"));
    report.hash =
      row.section === "current"
        ? row.id
        : `historical-n${row.n}-occurrence${row.component.split(",").at(-1)}`;
    element("detail-content").hidden = true;
    element("metadata").replaceChildren();
    element("coefficient-content").hidden = true;
    element("coefficient-body").replaceChildren();
    element("coefficient-actions").hidden = true;
    element("copy-fallback").hidden = true;
    element("coefficient-section").hidden = true;
    button("open-coefficients").textContent = "Open coefficients";
    button("open-coefficients").setAttribute("aria-expanded", "false");
    renderEntries();
    if (focus) {
      element("detail-title").focus();
    }
    void loadMetadata(row, selectionVersion);
  };
  /** Resolve existing case-page hashes as well as stable current/historical IDs. */
  const selectHash = () => {
    let hash;
    try {
      hash = decodeURIComponent(window.location.hash.slice(1));
    } catch {
      detailMessage.textContent =
        "The entry link is malformed. Select an entry from the catalogue.";
      return;
    }
    if (!hash) {
      return;
    }
    const row = entries.find(
      (item) =>
        item.id === hash ||
        item.legacy_anchor === hash ||
        (item.section === "current" &&
          item.kind === "polynomial" &&
          hash === `current-polynomial-for-n${item.n}`),
    );
    if (!row) {
      detailMessage.textContent =
        "This entry link is not in the catalogue. Search by case number or select an entry.";
      return;
    }
    section.value = row.section;
    kind.value = "all";
    status.value = "all";
    search.value = "";
    const position = entries.filter(matches).findIndex((item) => item.id === row.id);
    entryPage = Math.floor(Math.max(0, position) / entryBatch);
    selectEntry(row, false);
  };

  /** Insert exactly one batch of complete integer strings, including zeros. */
  const renderCoefficients = () => {
    if (!coefficients) {
      return;
    }
    const vector = coefficients.coefficients;
    const pages = Math.ceil(vector.length / coefficientBatch);
    const body = element("coefficient-body");
    body.replaceChildren();
    const start = coefficientPage * coefficientBatch;
    for (let index = start; index < Math.min(start + coefficientBatch, vector.length); index += 1) {
      const row = document.createElement("tr");
      const power = document.createElement("th");
      power.scope = "row";
      power.textContent = String(vector.length - 1 - index);
      const cell = document.createElement("td");
      const code = document.createElement("code");
      code.textContent = vector[index] ?? "";
      cell.append(code);
      row.append(power, cell);
      body.append(row);
    }
    element("coefficient-page").textContent = `Page ${coefficientPage + 1} of ${pages}`;
    coefficientMessage.textContent = `Coefficients ${start + 1}–${Math.min(start + coefficientBatch, vector.length)} of ${vector.length}. Descending powers; complete integer strings.`;
    button("previous-coefficients").disabled = coefficientPage === 0;
    button("next-coefficients").disabled = coefficientPage + 1 >= pages;
  };
  /** Keep async coefficient results attached to the selection that requested them. */
  const loadCoefficients = async () => {
    if (!selected?.coefficients_url) {
      return;
    }
    const row = selected;
    const url = selected.coefficients_url;
    const selection = selectionVersion;
    const version = ++coefficientVersion;
    coefficientAbort?.abort();
    const abort = new AbortController();
    coefficientAbort = abort;
    coefficientMessage.textContent = "Loading complete coefficient strings…";
    button("retry-coefficients").hidden = true;
    try {
      const value = await fetchJson(url, abort.signal);
      if (selection !== selectionVersion || version !== coefficientVersion) {
        return;
      }
      if (!coefficientPayload(value, row)) {
        throw new Error(
          "Coefficient JSON must contain the selected polynomial’s complete integer strings in descending order.",
        );
      }
      coefficients = value;
      renderEquation(row, value.coefficients);
      const download = /** @type {HTMLAnchorElement} */ (element("download-coefficients"));
      download.href = safeUrl(url);
      element("coefficient-actions").hidden = false;
      renderCoefficients();
    } catch (error) {
      if (
        selection === selectionVersion &&
        version === coefficientVersion &&
        !abort.signal.aborted
      ) {
        coefficientMessage.textContent = `Could not load coefficients: ${errorText(error)}. Retry or use the complete archives.`;
        button("retry-coefficients").hidden = false;
      }
    }
  };
  const copyCoefficients = async () => {
    if (!coefficients) {
      return;
    }
    const value = JSON.stringify(coefficients, null, 2);
    const version = selectionVersion;
    try {
      if (!navigator.clipboard) {
        throw new Error("Clipboard unavailable");
      }
      await navigator.clipboard.writeText(value);
      if (version === selectionVersion) {
        coefficientMessage.textContent =
          "Copied the complete coefficient JSON with every integer string.";
      }
    } catch {
      if (version === selectionVersion) {
        const text = /** @type {HTMLTextAreaElement} */ (element("coefficient-copy"));
        text.value = value;
        element("copy-fallback").hidden = false;
        text.focus();
        text.select();
        coefficientMessage.textContent =
          "Clipboard access unavailable. Copy the selected complete JSON below or download the file.";
      }
    }
  };
  const loadIndex = async () => {
    const version = ++indexVersion;
    indexMessage.textContent = "Loading the index…";
    button("retry-index").hidden = true;
    try {
      const loaded = readIndex(await fetchJson(root.dataset.indexUrl ?? "", undefined));
      if (version !== indexVersion) {
        return;
      }
      entries = loaded;
      status.replaceChildren(new Option("All statuses", "all"));
      for (const value of [...new Set(entries.map((row) => row.status))].sort()) {
        status.append(new Option(value, value));
      }
      renderEntries();
      selectHash();
    } catch (error) {
      if (version === indexVersion) {
        indexMessage.textContent = `Could not load the index: ${errorText(error)}. Retry or read the complete HTML archive above.`;
        button("retry-index").hidden = false;
      }
    }
  };

  const controls = /** @type {HTMLFormElement} */ (element("catalogue-controls"));
  controls.addEventListener("submit", (event) => event.preventDefault());
  for (const control of [search, section, kind, status]) {
    control.addEventListener(control === search ? "input" : "change", () => {
      entryPage = 0;
      renderEntries();
    });
  }
  button("clear-filters").addEventListener("click", () => {
    search.value = "";
    section.value = "current";
    kind.value = "all";
    status.value = "all";
    entryPage = 0;
    renderEntries();
  });
  button("previous-entries").addEventListener("click", () => {
    entryPage -= 1;
    renderEntries();
  });
  button("next-entries").addEventListener("click", () => {
    entryPage += 1;
    renderEntries();
  });
  button("retry-index").addEventListener("click", () => {
    void loadIndex();
  });
  button("retry-metadata").addEventListener("click", () => {
    if (selected) {
      selectEntry(selected, false);
    }
  });
  button("open-coefficients").addEventListener("click", () => {
    const content = element("coefficient-content");
    content.hidden = !content.hidden;
    button("open-coefficients").textContent = content.hidden
      ? "Open coefficients"
      : "Close coefficients";
    button("open-coefficients").setAttribute("aria-expanded", String(!content.hidden));
    if (!content.hidden && !coefficients) {
      void loadCoefficients();
    }
  });
  button("retry-coefficients").addEventListener("click", () => {
    void loadCoefficients();
  });
  button("previous-coefficients").addEventListener("click", () => {
    coefficientPage -= 1;
    renderCoefficients();
  });
  button("next-coefficients").addEventListener("click", () => {
    coefficientPage += 1;
    renderCoefficients();
  });
  button("copy-coefficients").addEventListener("click", () => {
    void copyCoefficients();
  });
  window.addEventListener("hashchange", selectHash);
  window.addEventListener("popstate", selectHash);
  void loadIndex();
})();
