# FN-1: original check2 input bytes

This adds the exact gzip files read by the eight check2 runs identified in
[jlevy/squares #366](https://github.com/jlevy/squares/issues/366#issuecomment-6026340743),
retained there at `2fad66e02f54a492835dc41ac37a9184e1e7a662`.
The files were copied without recompression.

The verifier hashes the raw input file bytes, before gzip decompression.
Thus `verifier_summary.premises.input_sha256` in each original receipt is the
SHA-256 of `check2/recorded-input.json.gz`, not of `candidate.json`.
For all eight files, decompression is byte-for-byte identical to the published
candidate; their mathematical candidate digests also match. This is a binding
record clarification, with no change to the certificates or lower bounds.
The n18=4.705 receipt already hashes the plain published candidate and needs
no additional file. These are distinct from the earlier n18=4.704 and
n19=4.8229 releases, which already include their exact compressed inputs.

[input-bindings.json](input-bindings.json) gives the compressed SHA-256,
decompressed SHA-256, mathematical candidate digest and repository-relative
paths. Existing candidates, logs, receipts and bundle archives are unchanged.
This supplement does not claim a new geometric verifier run.

From the repository root, verify the complete binding chain without running
the geometric verifier:

```sh
python3 - <<'PYTHON'
from pathlib import Path
import gzip, hashlib, json
sha = lambda b: hashlib.sha256(b).hexdigest()
m = json.loads(Path('verification/fn1/input-bindings.json').read_text())
keys = ['n', 'L', 'B', 'rectangles', 'points', 'total_mass', 'proof_net']
for e in m['entries']:
    raw = Path(e['input_file']).read_bytes()
    candidate = Path(e['published_candidate']).read_bytes()
    receipt = json.loads((Path(e['input_file']).parent / 'receipt.json').read_text())
    assert sha(raw) == e['compressed_sha256'] == receipt['verifier_summary']['premises']['input_sha256']
    assert gzip.decompress(raw) == candidate
    assert sha(candidate) == e['decompressed_sha256'] == receipt['file_sha256']
    d = json.loads(candidate)
    digest = sha(json.dumps({k: d[k] for k in keys}, sort_keys=True, separators=(',', ':')).encode())
    assert digest == e['candidate_digest'] == receipt['candidate_digest']
print('All 8 recorded inputs match their logs and published candidates')
PYTHON
```
