/** @param {HTMLElement} root */
(root) =>
  Array.from(
    root.querySelectorAll("a[id], a.github-dynamic-check, .site-colophon-line a"),
    (link) => {
      const before = getComputedStyle(link, "::before");
      const text = link.firstChild;
      const range = document.createRange();
      if (text instanceof Text && text.length > 0) {
        range.setStart(text, 0);
        range.setEnd(text, 1);
      }
      return {
        id: link.id,
        text: link.textContent,
        href: link.getAttribute("href"),
        display: getComputedStyle(link).display,
        content: before.content,
        beforeDisplay: before.display,
        afterContent: getComputedStyle(link, "::after").content,
        afterDisplay: getComputedStyle(link, "::after").display,
        mask: before.maskImage,
        color: getComputedStyle(link).color,
        ink: before.backgroundColor,
        width: Number.parseFloat(before.width),
        height: Number.parseFloat(before.height),
        lines: link.getClientRects().length,
        firstLineTop: link.getClientRects()[0]?.top,
        firstTextTop: range.getBoundingClientRect().top,
        svgs: link.querySelectorAll("svg").length,
        images: link.querySelectorAll("img").length,
      };
    },
  );
