import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";
import {
  assessCataloguePrecisionFrame,
  assessPackingSnapshot,
  CATALOGUE_PRECISION,
  PACKING_VALIDITY,
  type PackingSnapshot,
  workbenchCore,
} from "../src/core/runtime-contracts.ts";

interface FixtureCase {
  id: string;
  clause: string;
  tolerance: "contract" | "catalogue-precision";
  expectedCount: number;
  snapshot: PackingSnapshot;
  valid: boolean;
  geometryValid: boolean;
  reason: string | null;
}

interface Fixture {
  contract: string;
  tolerances: Record<string, number>;
  cases: FixtureCase[];
}

const SPELLED: Readonly<Record<string, number>> = {
  NaN: Number.NaN,
  Infinity: Number.POSITIVE_INFINITY,
  "-Infinity": Number.NEGATIVE_INFINITY,
};

function fixture(): Fixture {
  const text = readFileSync(new URL("fixtures/packing-validity.json", import.meta.url), "utf8");
  return JSON.parse(text, (_key, value: unknown) =>
    typeof value === "string" && value in SPELLED ? SPELLED[value] : value,
  ) as Fixture;
}

test("the shared fixture names the exported contract and its declared tolerances", () => {
  const cases = fixture();
  assert.equal(cases.contract, PACKING_VALIDITY.contract);
  assert.deepEqual(cases.tolerances, {
    contract: PACKING_VALIDITY.penetrationTolerance,
    "catalogue-precision": CATALOGUE_PRECISION.penetrationTolerance,
  });
  assert.equal(workbenchCore.PACKING_VALIDITY, PACKING_VALIDITY);
  assert.equal(workbenchCore.CATALOGUE_PRECISION, CATALOGUE_PRECISION);
});

test("every boundary case reaches the fixture's verdict and first failing clause", () => {
  const cases = fixture().cases;
  const clauses = new Set(cases.map((entry) => entry.clause));
  for (const clause of PACKING_VALIDITY.clauses) {
    assert(clauses.has(clause), `no boundary case exercises ${clause}`);
  }
  for (const entry of cases) {
    const assess =
      entry.tolerance === "contract" ? assessPackingSnapshot : assessCataloguePrecisionFrame;
    const assessment = assess(entry.snapshot, entry.expectedCount);
    assert.deepEqual(
      {
        valid: assessment.valid,
        geometryValid: assessment.geometryValid,
        reason: assessment.reason,
      },
      { valid: entry.valid, geometryValid: entry.geometryValid, reason: entry.reason },
      entry.id,
    );
    assert.equal(
      assessment.tolerance,
      entry.tolerance === "contract"
        ? PACKING_VALIDITY.penetrationTolerance
        : CATALOGUE_PRECISION.penetrationTolerance,
      `${entry.id} does not record the tolerance it applied`,
    );
  }
});
