/** A freshly cloned canonical article, with response-relative links and scoped IDs. */
interface SiteLoadedArticle {
  article: HTMLElement;
  responseUrl: string;
}

interface SiteArticlesApi {
  loadArticle(url: string, selector: string): Promise<SiteLoadedArticle>;
  returnFocus(opener: HTMLElement): HTMLElement;
  setReturnFocus(popover: HTMLElement, opener: HTMLElement): void;
  beginRequest(): number;
  isCurrent(request: number): boolean;
  cancelRequests(): void;
}

declare var siteArticles: SiteArticlesApi | undefined;
