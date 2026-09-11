// The two Node facilities the timeline harness uses, declared here rather than pulled in
// with `@types/node`.
//
// The harness is the one piece of JavaScript in this repository that runs under Node
// instead of in a browser, and it uses exactly two things Node provides: `require` for
// `node:fs`, and `process` for its arguments and its exit code. A whole type package for
// that is a dependency to pin, review and upgrade in exchange for two shapes; writing the
// two down says what is used and costs nothing to keep true.
//
// Everything else under this type gate is browser code, whose `lib` already covers it.

declare module "node:fs" {
  export function readFileSync(path: string, encoding: string): string;
}

declare const process: {
  argv: string[];
  exit(code: number): never;
};
