"""Write the packet's release-asset record from k1/large-verify.json and k1/release.json.

    python -I write_large_record.py K1_DIR OUT.json
"""

import json
import sys
from pathlib import Path

k1, out_path = Path(sys.argv[1]), Path(sys.argv[2])
v = json.loads((k1 / "large-verify.json").read_text())
rel = json.loads((k1 / "release.json").read_text())
out = {
    "format": "k17-release-assets-v1",
    "source_url": "https://github.com/Kleddamag/the-seventeenth-square-candidate",
    "release": {
        "tag": rel["tagName"],
        "name": rel["name"],
        "created_utc": rel["createdAt"],
        "published_utc": rel["publishedAt"],
        "target": rel["targetCommitish"],
        "url": "https://github.com/Kleddamag/the-seventeenth-square-candidate/releases/tag/large-files-v1",
        "notes_manifest_sha256": v["release"]["notes_manifest_sha256"],
        "notes_check_py_sha256": v["release"]["notes_check_py_sha256"],
    },
    "edition_commit": "653b9589d0f8a152f01adc56b1d48ba53d49abc3",
    "retrieved_at_utc": "2026-10-12T16:53Z",
    "how": (
        "Fetched with the author's fetch_large.py (read first; standard library, writes only "
        "under _large/) through gh release download, which reported FETCH RESULT: PASS; then "
        "re-hashed here with hashlib independently of that script. Each file's size and SHA-256 "
        "equal its LARGE_FILES.tsv row and the release's own asset digest. No asset is retained."
    ),
    "local_digests": {
        "MANIFEST.sha256": v["local"]["manifest_sha256"],
        "check.py": v["local"]["check_py_sha256"],
        "LARGE_FILES.tsv": v["local"]["large_files_tsv_sha256"],
        "manifest_matches_release_notes": v["local"]["manifest_matches_notes"],
        "check_py_matches_release_notes": v["local"]["check_py_matches_notes"],
    },
    "assets": [
        {
            "path": f["path"],
            "bytes": f["bytes"],
            "sha256": f["sha256"],
            "matches_large_files_tsv": f["matches_large_files_tsv"],
            "matches_release_asset_digest": f["matches_release_asset_digest"],
        }
        for f in v["files"]
    ],
    "total_bytes": v["total_bytes"],
    "all_match": v["all_match"],
}
out_path.write_text(json.dumps(out, indent=2) + "\n")
print(out["total_bytes"], out["all_match"], len(out["assets"]))
