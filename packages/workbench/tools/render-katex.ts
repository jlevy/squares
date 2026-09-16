import { pathToFileURL } from "node:url";

interface KatexOptions {
  throwOnError: boolean;
  output: "html";
  displayMode: boolean;
  strict: "error";
}

type RenderToString = (source: string, options: KatexOptions) => string;

async function readStandardInput(): Promise<string> {
  process.stdin.setEncoding("utf8");
  let input = "";
  for await (const chunk of process.stdin) {
    if (typeof chunk !== "string") {
      throw new TypeError("KaTeX input was not UTF-8 text");
    }
    input += chunk;
  }
  return input;
}

function stringArray(value: unknown): string[] {
  if (!Array.isArray(value) || !value.every((item) => typeof item === "string")) {
    throw new TypeError("KaTeX input must be a JSON array of strings");
  }
  return value;
}

const modulePath = process.argv[2];
if (modulePath === undefined) {
  throw new Error("usage: render-katex.ts KATEX_MODULE");
}

const loaded: unknown = await import(pathToFileURL(modulePath).href);
if (typeof loaded !== "object" || loaded === null) {
  throw new TypeError("KaTeX module has no exports");
}
const katex: unknown = Reflect.get(loaded, "default");
if (typeof katex !== "object" || katex === null) {
  throw new TypeError("KaTeX module has no default export");
}
const renderToString: unknown = Reflect.get(katex, "renderToString");
if (typeof renderToString !== "function") {
  throw new TypeError("KaTeX module has no renderToString function");
}

const sources = stringArray(JSON.parse(await readStandardInput()));
const options: KatexOptions = {
  throwOnError: true,
  output: "html",
  displayMode: false,
  strict: "error",
};
const rendered = sources.map((source) => (renderToString as RenderToString)(source, options));
process.stdout.write(JSON.stringify(rendered));
