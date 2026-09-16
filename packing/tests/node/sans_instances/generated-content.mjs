// `sans_instances/requests.js` over one element with a box and no text, whose
// pseudo-elements all compute the `content` handed in on argv as JSON
// `{content, pseudos}`. Prints `{rows, read}`: the requests the probe recorded, and the
// pseudo-element each `getComputedStyle` call asked for, in order.
import { probe } from "../probe.mjs";

/** @type {{ content: string, pseudos: string[] }} */
const { content, pseudos } = JSON.parse(process.argv[2] ?? "");

/** @type {(string | undefined)[]} */
const read = [];
const element = { getClientRects: () => [{}] };
Object.assign(globalThis, {
  NodeFilter: { SHOW_TEXT: 4 },
  document: {
    body: { querySelectorAll: () => [element] },
    createTreeWalker: () => ({ nextNode: () => null }),
  },
  /**
   * @param {object} _el
   * @param {string} [pseudo]
   */
  getComputedStyle: (_el, pseudo) => {
    read.push(pseudo);
    return {
      content,
      fontFamily: '"Print Sans", sans-serif',
      fontWeight: "400",
      fontStyle: "normal",
    };
  },
});

/** @type {(argument: [string[], string[], (el: object) => string]) => object[]} */
const requests = probe("devtools/probes/sans_instances/requests.js");
const rows = requests([["Print Sans"], pseudos, () => "div[0]"]);
process.stdout.write(JSON.stringify({ rows, read }));
