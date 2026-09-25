"""Reconstruct the pinned checker / 重建锁定的检查器。"""
from pathlib import Path
import hashlib
import json
import urllib.request

ROOT=Path(__file__).resolve().parent
URL='https://raw.githubusercontent.com/Guzhou0806/n17-square-packing/32edfd3da78bf80a309398f552b3b602b9c45d6c/certificates/R038/src/exact_parent_side_scan.js'
SOURCE='63e858e28c4dee40f5763a832e1cfdf1f1fce3a1e5c632d087525bf1ee20ed14'
FINAL='82fad041d66bc7a0f14d9dfe9b9282d8562d50fc4844649d2e684414a7ba24b1'


def need(ok,message):
    if not ok:raise ValueError(message+' / 重建检查失败')


def reconstruct(output,source=None):
    if source is None:
        with urllib.request.urlopen(URL,timeout=60) as stream:raw=stream.read()
    else:raw=Path(source).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==SOURCE,'Source SHA mismatch')
    for name in ['secondary-adaptation.json','r052-adaptation.json']:
        recipe=json.loads((ROOT/name).read_text(encoding='utf-8'))
        need(recipe['format']=='sha256-pinned-byte-edits-v1' and hashlib.sha256(raw).hexdigest()==recipe['source_sha256'],'Recipe source mismatch')
        parts=[];cursor=0
        for edit in recipe['edits']:
            a,b=edit['start'],edit['end']
            need(type(a) is int and type(b) is int and cursor<=a<=b<=len(raw),'Invalid edit')
            parts.extend([raw[cursor:a],edit['replacement'].encode('utf-8')]);cursor=b
        parts.append(raw[cursor:]);raw=b''.join(parts)
        need(hashlib.sha256(raw).hexdigest()==recipe['result_sha256'],'Recipe result mismatch')
    need(hashlib.sha256(raw).hexdigest()==FINAL,'Final checker mismatch')
    with Path(output).open('xb') as stream:stream.write(raw)
    return Path(output)
