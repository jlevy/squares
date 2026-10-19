// The archive's actual facets, disclosed cards, centered controls and shared meters.
/** @param {{ meters?: string, chooser?: string, choice?: string, overrideChooser?: boolean, meterSize?: string } | null} options */
async (options) => {
  const {
    meters = "",
    chooser = "",
    choice = "",
    overrideChooser = false,
    meterSize = "",
  } = options ?? {};
  const override = document.createElement("style");
  if (overrideChooser || meterSize) {
    override.textContent = meterSize
      ? `.site-significance { inline-size: ${meterSize} !important; }`
      : ".site-news-filters .site-tabs button { font-size: 40px !important; }";
    document.head.append(override);
  }
  if (chooser) {
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
    await new Promise((resolve) => requestAnimationFrame(() => resolve(undefined)));
  }
  /** @param {Element | null} element */
  const appearance = (element) => {
    if (!element) {
      return null;
    }
    const style = getComputedStyle(element);
    return Object.fromEntries(
      [
        "font-family",
        "font-size",
        "font-weight",
        "line-height",
        "letter-spacing",
        "text-transform",
        "font-variant-caps",
        "color",
        "background-color",
        "padding-top",
        "padding-right",
        "padding-bottom",
        "padding-left",
        "border-top-width",
        "border-bottom-width",
        "border-right-width",
        "border-top-color",
        "border-radius",
        "box-shadow",
        "outline-color",
        "outline-style",
        "outline-width",
        "text-decoration-line",
        "transition-property",
        "transition-duration",
        "transition-timing-function",
      ].map((name) => [name, style.getPropertyValue(name)]),
    );
  };
  const group = chooser ? document.querySelector(chooser) : null;
  const option = choice ? (group?.querySelector(choice) ?? null) : null;
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 1;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  /** @param {Element | null} element */
  const brightness = (element) => {
    if (!element || !context) {
      return null;
    }
    context.fillStyle = getComputedStyle(element).backgroundColor;
    context.fillRect(0, 0, 1, 1);
    const [red = 0, green = 0, blue = 0] = context.getImageData(0, 0, 1, 1).data;
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue;
  };
  /** WCAG relative luminance of a colour as the canvas paints it. @param {string} colour */
  const luminance = (colour) => {
    if (!context) {
      return 0;
    }
    context.clearRect(0, 0, 1, 1);
    context.fillStyle = colour;
    context.fillRect(0, 0, 1, 1);
    const channels = [...context.getImageData(0, 0, 1, 1).data.slice(0, 3)].map((value) => {
      const channel = value / 255;
      return channel <= 0.04045 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4;
    });
    const [red = 0, green = 0, blue = 0] = channels;
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue;
  };
  /** The WCAG contrast of two colours. @param {string} first @param {string} second */
  const contrast = (first, second) => {
    const [darker, lighter] = [luminance(first), luminance(second)].sort((a, b) => a - b);
    return ((lighter ?? 0) + 0.05) / ((darker ?? 0) + 0.05);
  };
  const check = option?.querySelector(".site-news-check") ?? null;
  const referenceChip = document.querySelector(
    `.site-news-topics [data-news-topic="${option?.getAttribute("data-news-topic")}"]`,
  );
  const neutral = document.createElement("span");
  neutral.className = "site-chip";
  group?.append(neutral);
  const neutralAppearance = appearance(neutral);
  neutral.remove();
  const count = document.querySelector(".site-table-tools .site-count");
  const countRow = count?.closest(".site-table-tools");
  const firstCard = document.querySelector("[data-news-day]:not([hidden])");

  const controls = document.querySelector("[data-news-filters]");
  const specimen = document.createElement("div");
  specimen.innerHTML = meters;
  document.querySelector(".site-page")?.append(specimen);
  const samples = [...specimen.querySelectorAll(".site-significance")].map((meter) => {
    const style = getComputedStyle(meter);
    const bars = [...meter.querySelectorAll(".site-significance-bar")];
    return {
      level: Number(meter.getAttribute("data-level")),
      label: meter.getAttribute("aria-label"),
      width: meter.getBoundingClientRect().width,
      font: Number.parseFloat(style.fontSize),
      border: Number.parseFloat(style.borderTopWidth),
      padding: Number.parseFloat(style.paddingLeft),
      fits: meter.scrollWidth <= meter.clientWidth,
      color: style.color,
      border_color: style.borderTopColor,
      side_space:
        (meter.firstElementChild?.getBoundingClientRect().left ?? 0) -
        meter.getBoundingClientRect().left +
        meter.getBoundingClientRect().right -
        (bars.at(-1)?.getBoundingClientRect().right ?? 0),
      filled: bars.filter((bar) => bar.getAttribute("data-filled") === "true").length,
      bars: bars.map((bar) => ({
        height: bar.getBoundingClientRect().height,
        width: bar.getBoundingClientRect().width,
        fill: getComputedStyle(bar).backgroundColor,
        border: Number.parseFloat(getComputedStyle(bar).borderTopWidth),
        filled: bar.getAttribute("data-filled") === "true",
      })),
    };
  });
  specimen.remove();
  const result = {
    chooser: group
      ? {
          appearance: appearance(option),
          brightness: brightness(option),
          check_visible: check ? getComputedStyle(check).visibility === "visible" : null,
          check_contrast:
            check && option
              ? contrast(getComputedStyle(check).color, getComputedStyle(option).backgroundColor)
              : null,
          chip_brightness: brightness(referenceChip),
          neutral: neutralAppearance,
          role: group.getAttribute("role"),
          focus_visible: option?.matches(":focus-visible"),
          selected: option?.getAttribute("aria-selected"),
          pressed: option?.getAttribute("aria-pressed"),
          border: getComputedStyle(group).borderTopWidth,
          gap: getComputedStyle(group).gap,
          height: option?.getBoundingClientRect().height,
          label:
            option?.querySelector("[data-news-topic-label]")?.textContent ?? option?.textContent,
          chip_label: document.querySelector(
            `.site-news-topics [data-news-topic="${option?.getAttribute("data-news-topic")}"]`,
          )?.textContent,
          chip: appearance(
            document.querySelector(
              `.site-news-topics [data-news-topic="${option?.getAttribute("data-news-topic")}"]`,
            ),
          ),
        }
      : null,
    count_style: appearance(count),
    count_right_gap:
      count && countRow
        ? countRow.getBoundingClientRect().right - count.getBoundingClientRect().right
        : null,
    count_card_right_gap:
      count && firstCard
        ? firstCard.getBoundingClientRect().right - count.getBoundingClientRect().right
        : null,
    count_above_cards:
      count && firstCard
        ? count.getBoundingClientRect().bottom < firstCard.getBoundingClientRect().top
        : null,
    groups: [...document.querySelectorAll("[data-news-filters] [role=group]")].map((item) => ({
      name: document.getElementById(item.getAttribute("aria-labelledby") || "")?.textContent,
      hidden_legend: document
        .getElementById(item.getAttribute("aria-labelledby") || "")
        ?.classList.contains("site-visually-hidden"),
      tabs: item.querySelectorAll("[role=tab]").length,
    })),
    scores: [
      ...(controls?.querySelectorAll('button[data-news-score][aria-pressed="true"]') ?? []),
    ].map((button) => button.getAttribute("data-news-score")),
    topics: [
      ...(controls?.querySelectorAll('button[data-news-topic][aria-pressed="true"]') ?? []),
    ].map((button) => button.getAttribute("data-news-topic")),
    topic_tallies: Object.fromEntries(
      [...(controls?.querySelectorAll("button[data-news-topic]") ?? [])].map((button) => [
        button.getAttribute("data-news-topic"),
        {
          label: button.querySelector("[data-news-topic-label]")?.textContent,
          name: button.textContent,
          tally: button.querySelector("[data-news-tally]")?.textContent,
        },
      ]),
    ),
    all_buttons: controls?.querySelectorAll("[data-news-all]").length,
    resets: [...(controls?.querySelectorAll("[data-news-reset]") ?? [])].map((button) => ({
      label: button.textContent,
      appearance: appearance(button),
    })),
    score_tooltips: Object.fromEntries(
      [...(controls?.querySelectorAll("[data-news-score]") ?? [])].map((button) => [
        button.getAttribute("data-news-score"),
        button.getAttribute("data-site-tooltip") || button.getAttribute("title"),
      ]),
    ),
    topic_palette: Object.fromEntries(
      [...document.querySelectorAll(".site-news-topics .site-chip, .site-chip[data-kind]")].map(
        (chip) => [
          chip.getAttribute("data-news-topic") || chip.getAttribute("data-kind"),
          getComputedStyle(chip).backgroundColor,
        ],
      ),
    ),
    controls_hidden: controls instanceof HTMLElement && controls.hidden,
    count: controls?.querySelector("[data-news-count]")?.textContent,
    empty:
      controls?.querySelector("[data-news-empty]") instanceof HTMLElement &&
      !controls.querySelector("[data-news-empty]")?.hasAttribute("hidden"),
    cards: [...document.querySelectorAll("[data-news-day]")].map((card) => {
      const box = card.getBoundingClientRect();
      const button = card.querySelector(".site-news-expand");
      const buttonBox = button?.getBoundingClientRect();
      const body = card.querySelector(".site-news-body");
      return {
        id: card.id,
        visible: card.getClientRects().length > 0,
        score: Number(card.getAttribute("data-news-score")),
        topics: (card.getAttribute("data-news-topics") || "").split(" ").filter(Boolean),
        expanded: button?.getAttribute("aria-expanded"),
        button_hidden: button instanceof HTMLButtonElement && button.hidden,
        center_offset: buttonBox
          ? (buttonBox.left + buttonBox.right - box.left - box.right) / 2
          : null,
        full: body instanceof HTMLElement && body.clientHeight >= body.scrollHeight - 1,
      };
    }),
    samples,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
  override.remove();
  return result;
};
