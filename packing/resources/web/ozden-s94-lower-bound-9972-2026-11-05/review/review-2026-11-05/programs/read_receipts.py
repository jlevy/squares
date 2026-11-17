"""Read the lab's native receipt archive as data (decides nothing about coverage).

Reads source/receipts/{INDEX.json.gz, selection.csv, directions.jsonl.gz} and
native/{A..F}.jsonl.gz with their summaries, and source/controls/native-mutant.jsonl
and control.json. It checks, against this review's own premises (premises.json):

- each stream's digests against the index, its rows' indices against its scope (each
  once), its summary file against the index's copy, its summary's premises and build;
- every row of every stream (selected or not) verified at threshold 1 with a finite
  bound >= 1, and which fields each stream's rows keep (the compaction);
- the merged archive: 4,972 lines, indices 0..4971 once, each line byte-identical to
  the line of the stream selection.csv names;
- E's scope against its stated formula, if the index states one, and F's scope;
- the mutant receipts' refusals and the stated witnesses (recomputed exactly by
  controls_exact.py, not here).

It also lists the lowest certified bounds, per stream, to choose sampled directions.

Usage: read_receipts.py PACKET_DIR PREMISES_JSON OUT_JSON
"""

from __future__ import annotations

import csv
import gzip
import json
import math
import sys
from collections import Counter
from pathlib import Path

from xzcommon import read_bytes, sha256


def main() -> int:
    packet = Path(sys.argv[1])
    prem = json.loads(Path(sys.argv[2]).read_text())
    out = Path(sys.argv[3])
    src = packet / "source"
    rec = src / "receipts"
    idx = json.loads(read_bytes(rec / "INDEX.json.gz"))
    checks: dict[str, bool] = {}
    rep: dict[str, object] = {"index_meaning": idx.get("meaning")}
    expected_premises = {
        "B": prem["B"],
        "D": prem["D"],
        "L": prem["L"],
        "angle_count": prem["N_theta"],
        "centre_domain": "per-bin",
        "expanded_points": 0,
        "expanded_rectangles": prem["expanded_rectangles"],
        "expanded_segments": 0,
        "format": "M",
        "input_sha256": prem["certificate_gz_sha256"],
        "mass_below_n": "1/100000",
        "mass_exact": prem["M"],
        "n": 94,
        "net_last_tangent": prem["t_max"],
        "net_origin": "proof_net",
        "shrink_bound": prem["N0b_B(1+D)"],
        "source_rectangles": prem["rows"],
    }
    lines_by_stream: dict[str, dict[int, bytes]] = {}
    fields_by_stream: dict[str, list[str]] = {}
    streams = []
    all_rows_ok = True
    for s in idx["sources"]:
        sid = s["id"]
        path = src / s["receipt_file"]
        raw = path.read_bytes()
        data = read_bytes(path)
        st = {
            "id": sid,
            "archive_sha256_matches_index": sha256(raw) == s["archive_sha256"],
            "uncompressed_sha256_matches_index": sha256(data) == s["uncompressed_sha256"],
        }
        lines = data.split(b"\n")
        if lines and lines[-1] == b"":
            lines = lines[:-1]
        parsed = [json.loads(x) for x in lines]
        summ_lines = [row for row in parsed if row.get("kind") == "sqverify-fast-summary/v1"]
        st["summary_lines_in_stream"] = len(summ_lines)
        st["summary_line_is_last"] = bool(parsed) and parsed[-1].get("kind") == "sqverify-fast-summary/v1"
        rows = [row for row in parsed if row.get("kind") != "sqverify-fast-summary/v1"]
        lines = [x for x, row in zip(lines, parsed, strict=True) if row.get("kind") != "sqverify-fast-summary/v1"]
        rs = [row["r"] for row in rows]
        st["rows"] = len(rows)
        st["scope_size"] = len(s["scope"])
        st["indices_equal_scope_once_each"] = sorted(rs) == sorted(s["scope"]) and len(set(rs)) == len(rs)
        st["row_count_matches_index"] = len(rows) == s["row_count"]
        ok = True
        least = math.inf
        least_r = None
        for row in rows:
            b = row.get("min_certified_lower_bound")
            good = (
                row.get("verdict") == "verified"
                and row.get("threshold") == "1"
                and isinstance(b, (int, float))
                and math.isfinite(b)
                and b >= 1
            )
            if not good:
                ok = False
            elif b < least:
                least, least_r = b, row["r"]
        st["every_row_verified_threshold_1_bound_ge_1"] = ok
        all_rows_ok = all_rows_ok and ok
        st["least_bound"] = least
        st["least_bound_r"] = least_r
        fc = Counter(tuple(sorted(row)) for row in rows)
        st["row_field_sets"] = [list(k) for k in fc]
        fields_by_stream[sid] = sorted({f for k in fc for f in k})
        methods = Counter(row.get("method") for row in rows)
        st["methods"] = dict(methods)
        st["nodes_recorded_sum"] = sum(row.get("nodes", 0) for row in rows)
        summ = json.loads((src / s["summary_file"]).read_text())
        st["summary_equals_index_copy"] = summ == s.get("summary", summ)
        st["summary_file_equals_stream_summary_line"] = len(summ_lines) == 1 and summ_lines[0] == summ
        st["summary_status"] = summ.get("status")
        st["summary_directions_equals_rows"] = summ.get("directions") == len(rows)
        st["summary_refused_empty"] = summ.get("refused_directions") == []
        st["summary_fault_null"] = summ.get("fault_injected_at_box") is None
        st["summary_threshold_1"] = summ.get("threshold") == "1"
        st["summary_premises_equal_recomputed"] = summ.get("premises") == expected_premises
        b = summ.get("build", {})
        st["summary_build"] = b
        st["summary_build_is_reviewed_source"] = (
            b.get("source_sha256") == "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88"
            and b.get("profile") == "release"
            and str(b.get("rustc", "")).startswith("rustc 1.98.0")
        )
        st["summary_threads"] = summ.get("threads")
        st["summary_nodes"] = summ.get("nodes")
        st["summary_direction_cpu_seconds"] = summ.get("direction_cpu_seconds")
        st["returncode"] = s.get("returncode")
        st["compaction"] = s.get("compaction")
        st["scope_kind"] = s.get("scope_kind")
        st["scope_min_max"] = [min(s["scope"]), max(s["scope"])]
        st["scope_residues_mod_3"] = dict(Counter(v % 3 for v in s["scope"]))
        for key in ("scope_formula", "formula", "declared", "sample", "note", "purpose"):
            if key in s:
                st[key] = s[key]
        streams.append(st)
        lines_by_stream[sid] = {row["r"]: line for row, line in zip(rows, lines, strict=True)}
        for key, val in st.items():
            if isinstance(val, bool):
                checks[f"{sid}:{key}"] = val
    rep["streams"] = streams
    rep["fields_by_stream"] = fields_by_stream
    checks["every_row_of_every_stream_verified"] = all_rows_ok

    # Selection and the merged archive.
    with (rec / "selection.csv").open() as fh:
        sel = {int(row["r"]): row["source"] for row in csv.DictReader(fh)}
    merged_raw = (rec / "directions.jsonl.gz").read_bytes()
    merged = read_bytes(rec / "directions.jsonl.gz")
    checks["merged_gzip_sha256_matches_index"] = sha256(merged_raw) == idx["merged_gzip_sha256"]
    checks["merged_jsonl_sha256_matches_index"] = sha256(merged) == idx["merged_jsonl_sha256"]
    mlines = merged.split(b"\n")
    if mlines and mlines[-1] == b"":
        mlines = mlines[:-1]
    mrows = [json.loads(x) for x in mlines]
    mr = [row["r"] for row in mrows]
    checks["merged_4972_lines"] = len(mrows) == 4972
    checks["merged_indices_0_to_4971_once"] = sorted(mr) == list(range(4972))
    checks["selection_covers_0_to_4971"] = sorted(sel) == list(range(4972))
    ident = all(lines_by_stream[sel[row["r"]]].get(row["r"]) == line for row, line in zip(mrows, mlines, strict=True))
    checks["merged_lines_byte_identical_to_selected_stream"] = ident
    checks["merged_every_line_verified_threshold_1_bound_ge_1"] = all(
        row.get("verdict") == "verified" and row.get("threshold") == "1" and row["min_certified_lower_bound"] >= 1
        for row in mrows
    )
    rep["selected_per_stream"] = dict(Counter(sel.values()))
    rep["merged_least_bound"] = min((row["min_certified_lower_bound"], row["r"]) for row in mrows)
    lows = sorted((row["min_certified_lower_bound"], row["r"], sel[row["r"]]) for row in mrows)
    rep["lowest_20_bounds"] = lows[:20]
    rep["lowest_by_stream"] = {
        sid: sorted((b, r) for b, r, ss in lows if ss == sid)[:5] for sid in "ABCDEF"
    }
    # Directions present in more than one stream, and agreement of their verdicts.
    multi = Counter(r for sid in lines_by_stream for r in lines_by_stream[sid])
    rep["directions_in_more_than_one_stream"] = sum(1 for v in multi.values() if v > 1)
    # Do the lab's own repeated runs of one direction agree (a determinism check)?
    rows_by_stream = {sid: {r: json.loads(line) for r, line in d.items()} for sid, d in lines_by_stream.items()}
    agree_bound = 0
    agree_nodes = 0
    nodes_compared = 0
    disagreements = []
    for r, cnt in multi.items():
        if cnt < 2:
            continue
        rows_r = [(sid, rows_by_stream[sid][r]) for sid in rows_by_stream if r in rows_by_stream[sid]]
        bounds = {row["min_certified_lower_bound"] for _, row in rows_r}
        if len(bounds) == 1:
            agree_bound += 1
        else:
            disagreements.append({"r": r, "rows": {sid: row["min_certified_lower_bound"] for sid, row in rows_r}})
        nodes = [row["nodes"] for _, row in rows_r if "nodes" in row]
        if len(nodes) >= 2:
            nodes_compared += 1
            agree_nodes += len(set(nodes)) == 1
    rep["repeated_directions_bound_equal"] = f"{agree_bound}/{sum(1 for v in multi.values() if v > 1)}"
    rep["repeated_directions_nodes_equal"] = f"{agree_nodes}/{nodes_compared}"
    rep["repeated_directions_disagreements"] = disagreements[:10]
    rep["repeated_directions_streams"] = dict(Counter("".join(sorted(sid for sid in rows_by_stream if r in rows_by_stream[sid])) for r, c in multi.items() if c > 1))
    e_scope = next(s["scope"] for s in idx["sources"] if s["id"] == "E")
    rep["E_scope"] = e_scope
    rep["E_scope_sorted_diffs"] = sorted(Counter(b - a for a, b in zip(sorted(e_scope), sorted(e_scope)[1:])).items())
    rep["E_selected"] = sorted(r for r, sid in sel.items() if sid == "E")
    rep["F_selected"] = sorted(r for r, sid in sel.items() if sid == "F")
    rep["axis_row"] = next(row for row in mrows if row["r"] == 0)
    rep["row_3663"] = next(row for row in mrows if row["r"] == 3663)
    rep["row_4971"] = next(row for row in mrows if row["r"] == 4971)
    rep["row_1198"] = next(row for row in mrows if row["r"] == 1198)
    # Mutant receipts (data).
    mut_lines = (src / "controls" / "native-mutant.jsonl").read_text().splitlines()
    rep["native_mutant_rows"] = [json.loads(x) for x in mut_lines]
    rep["control_json"] = json.loads((src / "controls" / "control.json").read_text())
    rep["checks"] = checks
    rep["all_checks_hold"] = all(checks.values())
    for key, val in checks.items():
        if not val:
            print("FAIL", key)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("streams", "E_scope", "control_json", "native_mutant_rows")}, indent=1, default=str)[:6000])
    out.write_text(json.dumps(rep, indent=1, default=str) + "\n")
    print("ALL_CHECKS_HOLD" if rep["all_checks_hold"] else "SOME_CHECK_FAILS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
