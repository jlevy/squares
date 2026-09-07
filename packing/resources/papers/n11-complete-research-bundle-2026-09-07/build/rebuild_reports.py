#!/usr/bin/env python3
"""Optional report rebuild; preserves delivered original files."""
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    base = Path(__file__).resolve().parents[1]
    out = base / 'rebuild'
    out.mkdir(exist_ok=True)
    for program in ('pandoc', 'pdflatex'):
        if shutil.which(program) is None:
            raise RuntimeError(f'Missing PDF build dependency: {program}')
    try:
        from pypdf import PdfWriter
    except ImportError as exc:
        raise RuntimeError('The optional PDF merge needs pypdf') from exc
    commands = [
        (base, ['pandoc', 'updates/enumeration_addendum.md', '-s', '--number-sections',
                '--toc', '--toc-depth=1', '--lua-filter=build/addendum_tables.lua',
                '-H', 'build/addendum_header.tex', '--pdf-engine=pdflatex',
                '-o', str(out/'enumeration_addendum.pdf')]),
        (base/'original_review', ['pandoc', 'n11_research_review.md', '-s', '--number-sections',
                '--toc', '--toc-depth=1', '--lua-filter=table_widths.lua',
                '-H', 'report_header.tex', '--pdf-engine=pdflatex',
                '-o', str(out/'original_review.pdf')]),
    ]
    for cwd, command in commands:
        subprocess.run(command, cwd=cwd, check=True, timeout=300)
    writer = PdfWriter()
    writer.append(str(out/'enumeration_addendum.pdf'), outline_item='Part I: Enumeration addendum')
    writer.append(str(out/'original_review.pdf'), outline_item='Part II: Original research review')
    with (out/'complete_review.pdf').open('wb') as f:
        writer.write(f)
    print(f'Rebuilt reports in {out}')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f'PDF rebuild failed: {exc}', file=sys.stderr)
        raise SystemExit(1)
