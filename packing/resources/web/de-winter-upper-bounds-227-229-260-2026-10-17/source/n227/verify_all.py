"""Replay every exact certificate using three exact geometry algorithms."""
from pathlib import Path
from fractions import Fraction
import hashlib,json
from verify_exact import certify
from verify_polygon_exact import check
from verify_polygon_clipping import check as check_clipped
root=Path(__file__).resolve().parent
manifest=json.loads((root/'records.json').read_text())
for record in manifest['records']:
    path=root/record['exact_file']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=record['exact_sha256']:
        raise ValueError('Exact witness hash mismatch')
    witness=json.loads(path.read_text())
    if witness['n']!=record['n']:
        raise ValueError('Witness count does not match manifest')
    if Fraction(witness['side'])>Fraction(record['decimal_upper_bound']):
        raise ValueError('Decimal bound is smaller than exact witness side')
    for validator in [certify,check,check_clipped]:
        result=validator(witness)
        if not result['valid'] or result['n']!=record['n']:
            raise ValueError('Geometry verification failed')
    print(json.dumps({'n':record['n'],'valid':True,'decimal_upper_bound':record['decimal_upper_bound'],'validators_passed':3}))
