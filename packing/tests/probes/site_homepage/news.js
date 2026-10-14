// The native News destinations and the actual entry card typography and bounds.
() => {
  const news = document.querySelector("[data-news]");
  const heading = document.querySelector("#news.site-title");
  if (!(news instanceof HTMLElement) || !(heading instanceof HTMLElement)) {
    throw new Error("News content and its shared heading must be present");
  }
  const headingStyle = getComputedStyle(heading);
  /** @param {Element} element */
  const typography = (element) => {
    const style = getComputedStyle(element);
    return {
      family: style.fontFamily,
      size: style.fontSize,
      weight: style.fontWeight,
      leading: style.lineHeight,
      color: style.color,
      spacing: style.letterSpacing,
      transform: style.textTransform,
      caps: style.fontVariantCaps,
    };
  };
  // Measure the page's ordinary H3 role outside News, without copying its CSS.
  const reference = document.createElement("h3");
  reference.textContent = "Reference heading";
  news.parentElement?.append(reference);
  const referenceH3 = typography(reference);
  reference.remove();
  return {
    reference_h3: referenceH3,
    text_color: getComputedStyle(news).color,
    family: getComputedStyle(news).fontFamily,
    heading: { family: headingStyle.fontFamily, transform: headingStyle.textTransform },
    entries: [...news.querySelectorAll("[data-news-entry]")].map((item) =>
      item.getAttribute("data-news-entry"),
    ),
    days: [...news.querySelectorAll("[data-news-day]")].map((day) => {
      const style = getComputedStyle(day);
      const box = day.getBoundingClientRect();
      const body = day.querySelector(".site-news-body");
      const prose = day.querySelector(".site-news-item p");
      const title = day.querySelector(".site-news-item h3");
      const date = day.querySelector("time");
      const topics = day.querySelector(".site-news-topics");
      const metadata = day.querySelector(".site-news-metadata");
      const meter = metadata?.querySelector(".site-significance");
      const meterBox = meter?.getBoundingClientRect();
      const chipBox = topics?.querySelector(".site-chip")?.getBoundingClientRect();
      const titleBox = title?.getBoundingClientRect();
      const topicBox = topics?.getBoundingClientRect();
      const button = day.querySelector(".site-news-expand");
      const arrow = button?.querySelector("[data-arrow]");
      return {
        id: day.id,
        date: day.getAttribute("data-news-day"),
        family: style.fontFamily,
        body_family: prose ? getComputedStyle(prose).fontFamily : null,
        body_height: body?.clientHeight ?? 0,
        body_scroll: body?.scrollHeight ?? 0,
        inline_height: body instanceof HTMLElement ? body.style.maxBlockSize : null,
        line_height: body ? Number.parseFloat(getComputedStyle(body).lineHeight) : 0,
        height: box.height,
        expanded: button?.getAttribute("aria-expanded"),
        button_hidden: button instanceof HTMLButtonElement && button.hidden,
        button_top: button?.getBoundingClientRect().top ?? 0,
        body_bottom: body?.getBoundingClientRect().bottom ?? 0,
        fade: body ? getComputedStyle(body, "::before").opacity : null,
        height_transition: body ? getComputedStyle(body).transitionProperty : null,
        arrow_transition: arrow ? getComputedStyle(arrow).transitionProperty : null,
        date_transform: date ? getComputedStyle(date).textTransform : null,
        title_transform: title ? getComputedStyle(title).textTransform : null,
        title_style: title ? typography(title) : null,
        topic_styles: [...(topics?.querySelectorAll(".site-chip") ?? [])].map(typography),
        title_before_date:
          !!date && !!titleBox && titleBox.bottom <= date.getBoundingClientRect().top,
        date_before_topics:
          !topicBox || (!!date && date.getBoundingClientRect().bottom <= topicBox.top),
        metadata_after_date: metadata?.previousElementSibling === date?.parentElement,
        meter_count: day.querySelectorAll(".site-significance").length,
        meter_label: meter?.getAttribute("aria-label"),
        meter_tooltip: meter?.getAttribute("data-site-tooltip") || meter?.getAttribute("title"),
        meter_right_gap:
          metadata && meterBox ? metadata.getBoundingClientRect().right - meterBox.right : null,
        meter_with_topics:
          !chipBox ||
          (!!meterBox && chipBox.top < meterBox.bottom && meterBox.top < chipBox.bottom),
        visible_rating_label: metadata?.querySelector(".site-news-significance")?.textContent,

        date_size: date ? Number.parseFloat(getComputedStyle(date).fontSize) : 0,
        title_size: title ? Number.parseFloat(getComputedStyle(title).fontSize) : 0,
        border: Number.parseFloat(style.borderTopWidth),
        left: box.left,
        right: box.right,
      };
    }),
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  };
};
