#!/usr/bin/env python3
"""Render a W5 wave-efficiency baseline from AgentSessions and their Codex receipts.

The agenda-013 and agenda-014 W5 reviews each needed the same table: one row per lane
with its terminal state, recorded cells, agent-active time, command time, model-stream
time, first-token wait, compaction, declared outputs and substantive outputs. Twice it was
assembled by reading receipt fields into a Markdown table by hand, which is the shape
`OR-1` forbids: a retained number whose tool does not exist. This is that tool.

Every figure is a field lookup or a count over the declared records:

- a **cell** is one entry in `session.workflow_phases`;
- an **output** is one path in `session.outputs`; a **substantive output** excludes the
  session's own record and every path under `campaign/resource-usage/`;
- **agent-active**, command, model-stream, first-token, compaction and response figures
  are the `delta` block of the `CodexTaskTreeDelta/v1` receipt the session declares.

Receipts are recursive task-tree intervals. A coordinator receipt that contains its
lanes' subtrees overlaps the lane receipts, so this tool prints the rows and refuses to
add a coordinator row into a lane total: pass `--lanes` for the rows to sum and
`--coordinator` for the row shown beside them. A session declaring zero or more than one
Codex receipt is refused rather than guessed at, and a receipt whose snapshot was still
live is marked as a lower bound.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_wave_efficiency \
        --lanes session-073 session-074 session-075 --coordinator session-072
    ... --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from devtools.render_pr_rollup import CODEX_CONTRACT, session_payloads
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
USAGE_PREFIX = "packing/campaign/resource-usage/"
TERMINAL = {"completed", "stopped"}
TOOL_CATEGORIES = ("command", "agent_wait", "file_change", "agent_control", "extension")


class RefusalError(ValueError):
    """The records do not support the number that was asked for."""


def _session(session_id: str) -> dict[str, Any]:
    matches = [payload for payload in session_payloads() if payload.get("id") == session_id]
    if len(matches) != 1:
        raise RefusalError(
            f"{session_id}: expected exactly one session record, found {len(matches)}"
        )
    return matches[0]


def _codex_receipt(session: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    references = [
        reference
        for reference in session.get("resource_rollups") or []
        if isinstance(reference, str) and reference.startswith(USAGE_PREFIX)
    ]
    receipts = []
    for reference in references:
        path = ROOT.parent / reference
        if not path.exists():
            raise RefusalError(f"{session['id']}: declares {reference}, which is not on disk")
        document = safe_load(path.read_text(encoding="utf-8"))
        meta = document.get("softschema") or {}
        if meta.get("contract") != CODEX_CONTRACT:
            continue
        receipts.append((reference, document["rollup"]))
    # The coordinator declares its lanes' receipts as well as its own; its own is the one
    # named for it. A lane declares exactly one.
    own = [
        item for item in receipts if Path(item[0]).stem == f"codex-task-tree-{session['id']}"
    ]
    if len(own) == 1:
        return own[0]
    if len(receipts) == 1:
        return receipts[0]
    raise RefusalError(
        f"{session['id']}: expected one Codex receipt named for the session, "
        f"found {len(receipts)} Codex receipts and none named for it"
    )


def lane_row(session_id: str) -> dict[str, Any]:
    """One measured row; every value is a lookup or a count, never an estimate."""
    session = _session(session_id)
    status = session.get("status")
    if status not in TERMINAL:
        raise RefusalError(f"{session_id}: status {status!r} is not terminal")
    reference, rollup = _codex_receipt(session)
    delta = rollup["delta"]
    tools = delta.get("tool_seconds_by_category") or {}
    outputs = [path for path in session.get("outputs") or [] if isinstance(path, str)]
    own_record = f"packing/campaign/agent-sessions/{session_id}-"
    substantive = [
        path
        for path in outputs
        if not path.startswith(own_record) and not path.startswith(USAGE_PREFIX)
    ]
    models = delta.get("models") or []
    return {
        "session": session_id,
        "title": session.get("title"),
        "status": status,
        "cells": len(session.get("workflow_phases") or []),
        "receipt": reference,
        "lower_bound": bool((rollup.get("completeness") or {}).get("snapshot_incomplete")),
        "start_cutoff_at": rollup["source"]["start_cutoff_at"],
        "end_cutoff_at": rollup["source"]["end_cutoff_at"],
        "agent_active_seconds": float(delta["agent_active_seconds"]),
        "active_union_seconds": float(delta["active_union_seconds"]),
        "parallel_overlap_seconds": float(delta["parallel_overlap_seconds"]),
        "timed_model_stream_seconds": float(delta["timed_model_stream_seconds"]),
        "recorded_first_token_wait_seconds": float(delta["recorded_first_token_wait_seconds"]),
        "compaction_seconds": float(delta["compaction_seconds"]),
        "compaction_event_count": int(delta["compaction_event_count"]),
        "tool_seconds": {
            category: float(tools.get(category, 0.0)) for category in TOOL_CATEGORIES
        },
        "model_response_count": sum(
            int(model.get("model_response_count") or 0) for model in models
        ),
        "output_tokens": sum(
            int((model.get("tokens") or {}).get("output") or 0) for model in models
        ),
        "thinking_levels": sorted(
            {
                f"{model.get('model')} @ {model.get('thinking_level')}"
                for model in models
                if model.get("model_response_count")
            }
        ),
        "outputs": len(outputs),
        "substantive_outputs": len(substantive),
    }


def _sum(rows: list[dict[str, Any]], key: str) -> float:
    return round(sum(float(row[key]) for row in rows), 3)


def baseline(lanes: list[str], coordinator: str | None) -> dict[str, Any]:
    lane_rows = [lane_row(session_id) for session_id in lanes]
    totals = {
        "cells": sum(row["cells"] for row in lane_rows),
        "agent_active_seconds": _sum(lane_rows, "agent_active_seconds"),
        "timed_model_stream_seconds": _sum(lane_rows, "timed_model_stream_seconds"),
        "recorded_first_token_wait_seconds": _sum(
            lane_rows, "recorded_first_token_wait_seconds"
        ),
        "compaction_seconds": _sum(lane_rows, "compaction_seconds"),
        "command_seconds": round(sum(row["tool_seconds"]["command"] for row in lane_rows), 3),
        "agent_wait_seconds": round(
            sum(row["tool_seconds"]["agent_wait"] for row in lane_rows), 3
        ),
        "model_response_count": sum(row["model_response_count"] for row in lane_rows),
        "outputs": sum(row["outputs"] for row in lane_rows),
        "substantive_outputs": sum(row["substantive_outputs"] for row in lane_rows),
        "lower_bound": any(row["lower_bound"] for row in lane_rows),
    }
    hours = totals["agent_active_seconds"] / 3600 if totals["agent_active_seconds"] else 0.0
    totals["outputs_per_active_hour"] = round(totals["outputs"] / hours, 3) if hours else None
    totals["substantive_per_active_hour"] = (
        round(totals["substantive_outputs"] / hours, 3) if hours else None
    )
    result: dict[str, Any] = {"lanes": lane_rows, "lane_totals": totals}
    if coordinator is not None:
        row = lane_row(coordinator)
        residual = row["agent_active_seconds"] - totals["agent_active_seconds"]
        result["coordinator"] = row
        # The coordinator interval contains the lane subtrees; the residual is what is
        # left after the lane receipts are removed, and it is approximate because the
        # four cutoffs differ and a lane receipt can be a lower bound.
        result["coordinator_residual_agent_active_seconds"] = round(residual, 3)
    return result


def _seconds(value: float) -> str:
    return f"{value:,.3f} s"


def render_markdown(result: dict[str, Any]) -> str:
    header = (
        "| Lane | Terminal state / cells | Agent-active | Command | Agent wait "
        "| Timed model stream | First-token wait | Compaction | Responses "
        "| Outputs / substantive |"
    )
    lines = [header, "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for row in result["lanes"]:
        bound = " (lower bound)" if row["lower_bound"] else ""
        lines.append(
            f"| {row['session']} | {row['status']} / {row['cells']} | "
            f"{_seconds(row['agent_active_seconds'])}{bound} | "
            f"{_seconds(row['tool_seconds']['command'])} | "
            f"{_seconds(row['tool_seconds']['agent_wait'])} | "
            f"{_seconds(row['timed_model_stream_seconds'])} | "
            f"{_seconds(row['recorded_first_token_wait_seconds'])} | "
            f"{_seconds(row['compaction_seconds'])} | {row['model_response_count']} | "
            f"{row['outputs']} / {row['substantive_outputs']} |"
        )
    totals = result["lane_totals"]
    bound = " (lower bound)" if totals["lower_bound"] else ""
    lines.append(
        f"| **Lane total** | **{totals['cells']} cells** | "
        f"**{_seconds(totals['agent_active_seconds'])}**{bound} | "
        f"**{_seconds(totals['command_seconds'])}** | "
        f"**{_seconds(totals['agent_wait_seconds'])}** | "
        f"**{_seconds(totals['timed_model_stream_seconds'])}** | "
        f"**{_seconds(totals['recorded_first_token_wait_seconds'])}** | "
        f"**{_seconds(totals['compaction_seconds'])}** | "
        f"**{totals['model_response_count']}** | "
        f"**{totals['outputs']} / {totals['substantive_outputs']}** |"
    )
    if "coordinator" in result:
        row = result["coordinator"]
        bound = " (lower bound)" if row["lower_bound"] else ""
        lines.append(
            f"| {row['session']} (coordinator, contains the lanes) | "
            f"{row['status']} / {row['cells']} | "
            f"{_seconds(row['agent_active_seconds'])}{bound} | "
            f"{_seconds(row['tool_seconds']['command'])} | "
            f"{_seconds(row['tool_seconds']['agent_wait'])} | "
            f"{_seconds(row['timed_model_stream_seconds'])} | "
            f"{_seconds(row['recorded_first_token_wait_seconds'])} | "
            f"{_seconds(row['compaction_seconds'])} | {row['model_response_count']} | "
            f"{row['outputs']} / {row['substantive_outputs']} |"
        )
    lines.append("")
    lines.append(
        f"Lane totals: {totals['outputs_per_active_hour']} declared output paths and "
        f"{totals['substantive_per_active_hour']} substantive paths per recursive "
        "agent-active hour."
    )
    if "coordinator" in result:
        lines.append(
            "Coordinator residual after removing the lane receipts: "
            f"{_seconds(result['coordinator_residual_agent_active_seconds'])} agent-active "
            "(approximate: the cutoffs differ and a lower-bound lane receipt understates "
            "its lane)."
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--lanes", nargs="+", required=True, help="lane session ids to sum")
    parser.add_argument(
        "--coordinator", help="coordinator session shown beside the lanes, never summed"
    )
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    options = parser.parse_args(argv)
    try:
        result = baseline(options.lanes, options.coordinator)
    except RefusalError as refusal:
        print(f"refused: {refusal}", file=sys.stderr)
        return 2
    if options.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
