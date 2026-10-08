/** Compact rows contain no coefficient vectors or typesetting payloads. */
interface ExactSideEntry {
  id: string;
  n: number;
  section: "current" | "historical";
  kind: "polynomial" | "numeric";
  component: string;
  title: string;
  status: string;
  degree: number | null;
  coefficient_digits: number | null;
  metadata_url: string;
  coefficients_url: string | null;
  legacy_anchor: string | null;
  search_text?: string;
}

/** Original register fields, rendered literally and fetched only on selection. */
interface ExactSideMetadata {
  schema_version: 1;
  id: string;
  claim: string;
  record: Record<string, unknown>;
}

/** Never parse coefficients as JavaScript numbers, including zero coefficients. */
interface ExactSideCoefficients {
  schema_version: 1;
  id: string;
  order: "descending";
  coefficients: string[];
}
