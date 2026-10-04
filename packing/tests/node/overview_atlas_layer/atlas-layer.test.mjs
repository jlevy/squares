// The atlas layer script's pure functions, run in a context with no document, as the view
// script's are: it publishes them on `globalThis.SiteAtlasLayer` and wires nothing until
// `atlas-grid.js` calls `mount`.
//
// They are what the address says about the drawing, how writing it leaves the rest of
// the address alone, including the view's own parameter, and which tab a key moves to.
// The browser tests (`tests/test_site_atlas_views.py`) hold the swap itself.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import vm from "node:vm";

/** @param {string} name */
const source = (name) =>
  readFileSync(new URL(`../../../devtools/overview/${name}`, import.meta.url), "utf8");

/** @returns {{ layer: SiteAtlasLayerApi, view: SiteAtlasViewApi }} */
function load() {
  const context = vm.createContext({ URLSearchParams });
  vm.runInContext(source("atlas-view.js"), context);
  vm.runInContext(source("atlas-layer.js"), context);
  return { layer: context.SiteAtlasLayer, view: context.SiteAtlasView };
}

const { layer, view } = load();

void test("the address names the regularized drawing and says nothing for house", () => {
  assert.equal(layer.layerOf(""), "house");
  assert.equal(layer.layerOf("?layer=regularized"), "regularized");
  assert.equal(layer.layerOf("?layer=house"), "house");
  assert.equal(layer.layerOf("?layer=Regularized"), "house");
  assert.equal(layer.layerOf("?layer=raw"), "house");
  assert.equal(layer.layerOf("?atlas=triangle&layer=regularized&age=180"), "regularized");
  assert.equal(layer.searchFor("", "regularized"), "?layer=regularized");
  assert.equal(layer.searchFor("?layer=regularized", "house"), "");
  assert.equal(layer.searchFor("", "house"), "");
});

void test("writing the drawing keeps every other parameter, and round-trips", () => {
  assert.equal(layer.searchFor("?age=180", "regularized"), "?age=180&layer=regularized");
  assert.equal(layer.searchFor("?layer=regularized&age=180", "house"), "?age=180");
  for (const search of ["", "?age=180", "?layer=regularized", "?x=1&layer=house"]) {
    for (const drawing of /** @type {AtlasLayer[]} */ (["house", "regularized"])) {
      assert.equal(layer.layerOf(layer.searchFor(search, drawing)), drawing);
    }
  }
});

void test("the view and the drawing are two parameters that never overwrite each other", () => {
  let search = "?age=180";
  search = view.searchFor(search, "triangle");
  search = layer.searchFor(search, "regularized");
  assert.equal(search, "?age=180&atlas=triangle&layer=regularized");
  assert.equal(view.viewOf(search), "triangle");
  assert.equal(layer.layerOf(search), "regularized");
  search = view.searchFor(search, "grid");
  assert.equal(search, "?age=180&layer=regularized");
  assert.equal(layer.layerOf(search), "regularized");
  search = layer.searchFor(search, "house");
  assert.equal(search, "?age=180");
  assert.equal(view.viewOf(search), "grid");
});

void test("the arrow keys wrap between the two tabs, Home and End go to the ends", () => {
  assert.equal(layer.stepTo("ArrowRight", 0, 2), 1);
  assert.equal(layer.stepTo("ArrowRight", 1, 2), 0);
  assert.equal(layer.stepTo("ArrowLeft", 0, 2), 1);
  assert.equal(layer.stepTo("ArrowLeft", 1, 2), 0);
  assert.equal(layer.stepTo("Home", 1, 2), 0);
  assert.equal(layer.stepTo("End", 0, 2), 1);
  assert.equal(layer.stepTo("ArrowDown", 0, 2), -1);
  assert.equal(layer.stepTo("Enter", 0, 2), -1);
  assert.equal(layer.stepTo("ArrowRight", -1, 2), -1);
  assert.equal(layer.stepTo("ArrowRight", 0, 0), -1);
});
