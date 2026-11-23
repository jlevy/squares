"""Unpack the bundled Python sources and launch the public verifier."""
import json
from pathlib import Path
from shutil import copyfile
import subprocess
import sys
from tempfile import TemporaryDirectory

here=Path(__file__).resolve().parent
with TemporaryDirectory()as tmp:
    d=Path(tmp)
    for name,code in json.loads((here/'replay_sources.json').read_text()).items():
        assert name==Path(name).name and name.endswith('.py')
        (d/name).write_text(code)
    copyfile(here/'certificate.json',d/'certificate.json')
    raise SystemExit(subprocess.run([sys.executable,'-B',d/'verify_public.py',*sys.argv[1:]]).returncode)
