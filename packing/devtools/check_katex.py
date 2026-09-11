"""Parse Markdown mathematics with the KaTeX bundle pinned through kpress.

Run from packing/: python -m devtools.check_katex FILE...

This reads files only. It reuses check_math_spans' dollar-delimiter and code-masking
rules, so its scope is recognized $...$ and $$...$$ spans, not delimiter linting or
browser layout. Every input must contain mathematics. Unsupported syntax, strict-mode
warnings, missing inputs, and an unavailable renderer fail the check. No network or
browser is involved. The renderer controls in test_check_katex run in the fast suite.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict, cast

from devtools.check_math_spans import math_spans_with_mode
from devtools.render_explainer import kpress_static


class ParseError(TypedDict):
    span: int
    source: str
    error: str


class FileReport(TypedDict):
    path: str
    spans: int
    errors: list[ParseError]


class Report(TypedDict):
    version: str
    files: list[FileReport]


class Span(TypedDict):
    source: str
    display: bool


PARSE = r"""
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const katex = require(input.bundle);
const files = input.files.map(file => {
  const errors = [];
  file.spans.forEach((span, index) => {
    const source = span.source;
    try {
      katex.renderToString(source, {
        displayMode: span.display, throwOnError: true, strict: 'error', trust: false
      });
    } catch (error) {
      errors.push({span: index + 1, source, error: String(error)});
    }
  });
  return {path: file.path, spans: file.spans.length, errors};
});
process.stdout.write(JSON.stringify({version: katex.version, files}));
"""


def check_files(paths: Sequence[Path]) -> Report:
    """Require math in every input and ask the pinned renderer to parse every span."""
    if not paths:
        raise ValueError("at least one Markdown file is required")
    files: list[dict[str, str | list[Span]]] = []
    for path in paths:
        spans: list[Span] = [
            {"source": source, "display": display}
            for source, display in math_spans_with_mode(path.read_text(encoding="utf-8"))
        ]
        if not spans:
            raise ValueError(f"{path}: no mathematical spans found")
        files.append({"path": str(path), "spans": spans})
    node = shutil.which("node")
    if node is None:
        raise ValueError("Node.js is required to run the pinned KaTeX bundle")
    bundle = kpress_static() / "katex" / "katex.min.js"
    result = subprocess.run(
        [node, "-e", PARSE],
        input=json.dumps({"bundle": str(bundle), "files": files}),
        text=True,
        capture_output=True,
        check=True,
        timeout=60,
    )
    return cast(Report, json.loads(result.stdout))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)
    try:
        report = check_files(args.files)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"KaTeX check unavailable: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return int(any(file["errors"] for file in report["files"]))


if __name__ == "__main__":
    raise SystemExit(main())
