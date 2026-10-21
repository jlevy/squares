/** A freshly cloned canonical article, with response-relative links and scoped IDs. */
interface SiteLoadedArticle {
  article: HTMLElement;
  responseUrl: string;
}

interface SiteArticlesApi {
  loadArticle(url: string, selector: string): Promise<SiteLoadedArticle>;
  /** Run `step` on every clone `loadArticle` returns from now on, before its consumer. */
  prepare(step: (article: HTMLElement) => void): void;
  /**
   * The element an unmodified primary click or press landed on; null when a modifier key,
   * another button or an earlier listener has claimed it, which the overlays leave alone.
   */
  clickTarget(event: MouseEvent): Element | null;
  returnFocus(opener: HTMLElement): HTMLElement;
  setReturnFocus(popover: HTMLElement, opener: HTMLElement): void;
  beginRequest(): number;
  isCurrent(request: number): boolean;
  cancelRequests(): void;
}

declare var siteArticles: SiteArticlesApi | undefined;
