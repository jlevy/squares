"""Write a freeze receipt: SHA-256 of the named files and a UTC timestamp.

Usage: python -I l82_freeze.py OUT.json LABEL FILE...
"""

import datetime
import hashlib
import json
import os
import sys

out, label, files = sys.argv[1], sys.argv[2], sys.argv[3:]
rec = {
    "label": label,
    "frozen_at_utc": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "sha256": {os.path.basename(f): hashlib.sha256(open(f, "rb").read()).hexdigest() for f in files},
}
with open(out, "w") as fh:
    json.dump(rec, fh, indent=1)
    fh.write("\n")
print(json.dumps(rec, indent=1))
