// Input-independent application startup: load and validate the published corpus before
// starting the application. The offline candidate continues to carry its own corpus.
import { decodeCorpus } from "./data/corpus.ts";

export async function loadCorpus(url: URL, origin = location.origin): Promise<unknown> {
  if (url.origin !== origin) {
    throw new Error("The packing data must be served by this site.");
  }
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Packing data request failed (HTTP ${response.status}).`);
  }
  return decodeCorpus(await response.json());
}

export async function startPublished(): Promise<void> {
  const island = document.getElementById("atlas-data");
  const source = island?.getAttribute("data-src");
  const application = island?.getAttribute("data-application-src");
  if (!island || !source || !application) {
    throw new Error("The workbench is missing its startup manifest.");
  }
  const data = await loadCorpus(new URL(source, document.baseURI));
  island.textContent = JSON.stringify(data);
  const script = document.createElement("script");
  const scriptUrl = new URL(application, document.baseURI);
  if (scriptUrl.origin !== location.origin) {
    throw new Error("The application must be served by this site.");
  }
  script.src = scriptUrl.href;
  await new Promise<void>((resolve, reject) => {
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("The workbench application could not be loaded."));
    document.body.append(script);
  });
  document.getElementById("workbench-startup")?.remove();
}

if (typeof document !== "undefined") {
  void startPublished().catch((error: unknown) => {
    const message = error instanceof Error ? error.message : String(error);
    const status = document.getElementById("workbench-startup");
    if (status) {
      status.setAttribute("role", "alert");
      status.textContent = `Unable to open the workbench. ${message} Reload the page to try again.`;
    }
  });
}
