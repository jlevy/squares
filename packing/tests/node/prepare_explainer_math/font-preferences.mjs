// The head script `font_preference_html` injects (`prepare_explainer_math/font_preferences.js`,
// applied), read from stdin and run against a stand-in root element. Prints the root's data
// attributes afterwards, as JSON, for the test to compare with the preferences it asked for.
import { readFileSync } from "node:fs";
import { runInThisContext } from "node:vm";

/** @type {Record<string, string>} */
const dataset = {};
Object.assign(globalThis, { document: { documentElement: { dataset } } });
runInThisContext(readFileSync(0, "utf8"));
process.stdout.write(JSON.stringify(dataset));
