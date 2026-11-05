#!/usr/bin/env python3
"""Audit retained bytes and exact premises; this is not a numerical full-net replay."""
import argparse
import csv
from fractions import Fraction as F
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys
import zlib

from rescale import (ROOT, CANDIDATE_GZIP, CANDIDATE_JSON, VERIFIER_SOURCE,
                     PacketError, deterministic_gzip, regenerate, require, sha, source_digest)
sys.path.insert(0, str(ROOT/'exploratory'))
import prep

def load_json(path):
    return json.loads(path.read_text(), parse_constant=lambda text: (_ for _ in ()).throw(
        PacketError('nonfinite_json', text)))

def check_premises(summary, candidate_sha, mass):
    require(summary['kind'] == 'sqverify-fast-summary/v1', 'native_kind', 'unknown native summary')
    require(summary['threshold'] == '1', 'native_threshold', 'threshold must be exactly 1')
    require(summary['build']['source_sha256'] == VERIFIER_SOURCE, 'native_source', 'wrong native verifier')
    p = summary['premises']
    require(p['input_sha256'] == candidate_sha, 'native_input', 'wrong input digest')
    require(p['n'] == 94 and p['angle_count'] == 4972 and p['format'] == 'M' and
            p['centre_domain'] == 'per-bin' and p['net_origin'] == 'proof_net',
            'native_domain', 'unexpected native domain/net')
    expected = {'L': F(2493,250), 'B': F(24872661,24875000), 'D': F(1,12000),
                'mass_exact': mass, 'mass_below_n': 94-mass,
                'net_last_tangent': F(1657,4000), 'shrink_bound': F(99498934887,99500000000)}
    require(all(F(p[key]) == value for key,value in expected.items()), 'native_premises', 'native premise mismatch')
    require(p['source_rectangles'] == 853 and p['expanded_rectangles'] == 6720 and
            p['expanded_points'] == 0 and p['expanded_segments'] == 0,
            'native_geometry', 'unexpected native geometry')
    require(summary['fault_injected_at_box'] is None, 'native_fault', 'fault injection present')

def native_stream(raw):
    parsed = []
    for line in raw.splitlines(keepends=True):
        require(line.startswith(b'{'), 'native_stream', 'unexpected non-JSON native line')
        obj = json.loads(line, parse_constant=lambda text: (_ for _ in ()).throw(PacketError('nonfinite_json', text)))
        parsed.append((obj,line))
    summaries = [obj for obj,_ in parsed if obj.get('kind') == 'sqverify-fast-summary/v1']
    require(len(summaries) == 1 and parsed[-1][0] == summaries[0], 'native_summary', 'expected one terminal summary')
    return [(obj,line) for obj,line in parsed if 'r' in obj], summaries[0]

def check_row(row):
    require(type(row['r']) is int and 0 <= row['r'] < 4972, 'direction_index', 'invalid direction')
    require(row['verdict'] == 'verified' and row['threshold'] == '1', 'native_verdict', 'direction not verified at 1')
    value = row['min_certified_lower_bound']
    require(type(value) in (int,float) and math.isfinite(value) and value >= 1,
            'native_bound', 'bound must be a finite number >= 1')
    require(row['method'] in ('axis-vertex-sweep', 'interval-branch-and-bound'), 'native_method', 'unknown native method')

def native_domain_margin(r, step):
    a = max(F(0), r*step-step/2)
    return (1+2*a-a*a)/(2*(1+a*a))

def native_exact_admission(P):
    L,B,D = P['L'],P['B'],P['D']
    count = P['last']+1
    tangent_shrink = B*(1+D/(1-D*D/4))
    require(0 < P['M'] < P['n'] and 0 < L <= 1000 and L*L >= 2*B*B and
            2 <= count <= 2**16 and len(P['rects']) <= 10**6 and tangent_shrink < 1,
            'native_exact_admission', 'native size/net/tangent-shrink premise failed')
    expanded = {}
    for x1,y1,x2,y2,w in P['rects']:
        density = w/(8*(x2-x1)*(y2-y1))
        for rectangle in prep.d4_images(x1,y1,x2,y2,L):
            expanded[rectangle] = expanded.get(rectangle,F(0))+density
    require(len(expanded) == 6720 and max(expanded.values()) <= 2**96,
            'native_density_cap', 'expanded native density/count mismatch')
    expanded_mass = sum(density*(x2-x1)*(y2-y1) for (x1,y1,x2,y2),density in expanded.items())
    require(expanded_mass == P['M'], 'native_expanded_mass', 'D4 expansion changed mass')
    require(all(L/2 < L-native_domain_margin(r,D) for r in range(count)),
            'native_domain_nonempty', 'native centre domain empty')
    return dict(tangent_shrink_bound=str(tangent_shrink),tangent_shrink_lt_one=True,
                side_and_primitive_caps_hold=True,expanded_rectangles=len(expanded),
                density_cap_log2=96,expanded_mass=str(expanded_mass),native_domains_nonempty=True)

def check_exact_witness(P, r, x, y, expected):
    margin = native_domain_margin(r, P['D'])
    require(P['L']/2 <= x <= P['L']-margin and P['L']/2 <= y <= P['L']-margin,
            'witness_domain', 'exact witness outside native checked quadrant')
    capture = prep.exact_F(P, r, x, y)
    require(capture == F(expected) and capture < 1, 'witness_capture', 'exact capture mismatch/not below 1')
    return capture

def audit(check_manifest=True):
    if check_manifest:
        manifest = load_json(ROOT/'MANIFEST.json')
        require(manifest['kind'] == 'sha256-file-manifest/v1', 'manifest_kind', 'unknown manifest')
        for name,digest in manifest['files'].items():
            path = Path(name)
            require(not path.is_absolute() and '..' not in path.parts, 'manifest_path', 'unsafe path')
            require(sha((ROOT/path).read_bytes()) == digest, 'manifest_digest', name)
        require(manifest['files']['LICENSE.md'] == '5b8e14499bddd521ce875b7b1b30da6f7ea215f3c44e15cfabce3a493f18da4c',
                'license_digest', 'license must match existing declaration byte for byte')
        observed_files = set()
        for path in ROOT.rglob('*'):
            rel = path.relative_to(ROOT)
            if rel.parts[0] == '.git' or '__pycache__' in rel.parts or rel.parts[:3] == ('verifier','sqverify_fast','target'):
                continue
            require(not path.is_symlink(), 'packet_symlink', str(rel))
            if path.is_file() and str(rel) != 'MANIFEST.json':observed_files.add(str(rel))
        require(observed_files == set(manifest['files']), 'manifest_file_set', 'unexpected or missing packet file')
    raw, compressed = regenerate()
    require((ROOT/'certificate/n94-L9972.json').read_bytes() == raw and
            (ROOT/'certificate/n94-L9972.json.gz').read_bytes() == compressed,
            'certificate_bytes', 'retained certificate differs from regenerated bytes')
    require(source_digest() == VERIFIER_SOURCE, 'source_digest', 'verifier source changed')
    provenance = load_json(ROOT/'verifier/PROVENANCE.json')
    require(provenance['commit'] == 'e6e8d57726db80cd0e6a1523166a96c5d36a3119', 'source_pin', 'wrong upstream pin')
    for entry in provenance['files']:
        data = (ROOT/'verifier/sqverify_fast'/entry['path']).read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob == entry['git_blob_sha1'] and sha(data) == entry['sha256'], 'source_blob', entry['path'])
    candidate = json.loads(raw)
    require(candidate['n'] == 94 and candidate['proof_net'] == {'last':4971, 'step':'1/12000'} and
            len(candidate['rectangles']) == 853 and candidate['points'] == [] and not candidate.get('segments'),
            'certificate_shape', 'unexpected input shape')
    ok,info,P = prep.premises(candidate)
    require(ok and P['L'] == F(2493,250) and P['B'] == F(24872661,24875000) and P['M'] == F(9399999,100000),
            'exact_premises', 'exact premises failed')
    source = json.loads(gzip.decompress((ROOT/'source/hosono-candidate.json.gz').read_bytes()))
    lam = F(4986,4975)
    require(len(source['rectangles']) == len(candidate['rectangles']), 'rescale_rows', 'row count changed')
    for old,new in zip(source['rectangles'],candidate['rectangles']):
        require(F(old['mass']) == F(new['mass']) and
                [F(x)*lam for x in old['rectangle']] == [F(x) for x in new['rectangle']],
                'exact_rescale', 'coordinate scaling or unchanged mass violated')
    native_admission = native_exact_admission(P)
    index = load_json(ROOT/'receipts/INDEX.json')
    require(index['kind'] == 'native-receipt-index/v1' and index['directions'] == 4972,
            'index_kind', 'unknown receipt index')
    streams,source_stats = {},[]
    for ev in index['sources']:
        require(ev['id'] not in streams, 'duplicate_source', ev['id'])
        archive = (ROOT/ev['receipt_file']).read_bytes()
        original = gzip.decompress(archive)
        require(sha(archive) == ev['archive_sha256'] and sha(original) == ev['uncompressed_sha256'],
                'native_archive_digest', ev['id'])
        rows,summary = native_stream(original)
        require(summary == load_json(ROOT/ev['summary_file']), 'summary_copy', ev['id'])
        check_premises(summary,CANDIDATE_GZIP,P['M'])
        require(ev['returncode'] == 0 and summary['status'] == 'PARTIAL' and summary['refused_directions'] == [],
                'native_status', ev['id'])
        for row,_ in rows: check_row(row)
        observed = [row['r'] for row,_ in rows]
        require(len(observed) == len(set(observed)) and sorted(observed) == ev['scope'] and
                len(observed) == ev['row_count'] == summary['directions'], 'native_scope', ev['id'])
        if 'compaction' in ev:
            comp = ev['compaction']
            require(comp['directions'] == len(rows), 'compaction_count', ev['id'])
            for row,_ in rows:
                require(set(row) <= set(comp['retained_fields']), 'compaction_fields', ev['id'])
        streams[ev['id']] = {row['r']:(row,line) for row,line in rows}
        source_stats.append(dict(id=ev['id'],reported=len(rows),selected=ev['selected']))
    require(set(streams) == set('ABCDEF'), 'source_set', 'expected exactly six native streams')
    require(sorted(streams['A']) == list(range(2486,4972)) and sorted(streams['F']) == [0,1198],
            'declared_scope', 'upper slice/positive-control scope differs')
    probe_scope = sorted({round(F(4971*k,128)) for k in range(129)} | set(range(20)) | {1195,2590})
    require(sorted(streams['E']) == probe_scope, 'probe_scope', 'sample does not match original formula')
    covered_before = set(streams['A']) | set(streams['E']) | set(streams['F'])
    missing = sorted(set(range(4972))-covered_before)
    for i,label in enumerate('BCD'):
        require(sorted(streams[label]) == missing[i::3], 'explicit_scope_partition', label)
    merged_archive = (ROOT/index['merged']).read_bytes(); merged = gzip.decompress(merged_archive)
    require(sha(merged_archive) == index['merged_gzip_sha256'] and sha(merged) == index['merged_jsonl_sha256'],
            'merged_digest', 'merged archive digest mismatch')
    final_rows = [(json.loads(line),line) for line in merged.splitlines(keepends=True)]
    require([row['r'] for row,_ in final_rows] == list(range(4972)), 'exhaustive_unique', 'need exactly r=0..4971 in order')
    with (ROOT/index['selection']).open(newline='') as stream:
        selected = list(csv.DictReader(stream))
    require(len(selected) == 4972, 'selection_count', 'wrong selection length')
    selected_counts = {label:0 for label in streams}
    for i,((row,line),choice) in enumerate(zip(final_rows, selected)):
        check_row(row)
        require(choice['r'] == str(i) and choice['source'] in streams, 'selection_index', 'bad selection row')
        label = choice['source']
        require(i in streams[label] and line == streams[label][i][1], 'native_line_identity', str(i))
        selected_counts[label] += 1
    require(all(selected_counts[ev['id']] == ev['selected'] for ev in index['sources']),
            'selection_totals', 'selection totals mismatch')
    mutant_archive = (ROOT/'controls/mass-99-100.json.gz').read_bytes()
    mutant = json.loads(gzip.decompress(mutant_archive))
    expected = dict(candidate)
    expected['rectangles'] = [dict(rectangle=row['rectangle'],mass=str(F(row['mass'])*F(99,100))) for row in candidate['rectangles']]
    expected['total_mass'] = str(sum(F(row['mass']) for row in expected['rectangles']))
    expected['derived_from'] = 'NEGATIVE CONTROL: verified n94 L9.972 certificate, every mass multiplied by99/100'
    require(mutant == expected and mutant_archive == deterministic_gzip(json.dumps(expected,sort_keys=True,separators=(',',':')).encode()),
            'mutant_construction', 'mutant is not exact 99/100 mass construction')
    ok,_,mutant_P = prep.premises(mutant)
    require(ok, 'mutant_premises', 'mutant premises failed')
    native_exact_admission(mutant_P)
    control = load_json(ROOT/'controls/control.json')
    require(control['status'] == 'CONTROL_PASSED' and control['mass_multiplier'] == '99/100', 'control_status', 'control failed')
    for label in ['positive','mutant']:
        record = control['independent'][label]
        require(record['sha256'] == (CANDIDATE_GZIP if label == 'positive' else sha(mutant_archive)), 'control_input', label)
        check_premises(record['summary'], record['sha256'], P['M'] if label == 'positive' else mutant_P['M'])
    negative_rows,negative_summary = native_stream((ROOT/'controls/native-mutant.jsonl').read_bytes())
    require(negative_summary == control['independent']['mutant']['summary'] and
            control['independent']['mutant']['returncode'] == 1 and negative_summary['status'] == 'REFUSED' and
            negative_summary['refused_directions'] == [0,1198] and sorted(row['r'] for row,_ in negative_rows) == [0,1198] and
            all(row['verdict'] != 'verified' for row,_ in negative_rows), 'mutant_native_refusal', 'negative control not refused')
    require(control['independent']['positive']['returncode'] == 0 and
            control['independent']['positive']['summary'] == load_json(ROOT/'receipts/native/F.summary.json'),
            'positive_native', 'positive control mismatch')
    witness = control['exact_counterexample']
    value = check_exact_witness(mutant_P, witness['r'], F(witness['x']), F(witness['y']), witness['capture'])
    native_witnesses = 0
    for row,_ in negative_rows:
        if 'witness' in row:
            w = row['witness']
            require(w['exact_below_threshold'] is True and w['exact_pose'] == [w['x'],w['y']], 'native_witness', 'bad witness metadata')
            check_exact_witness(mutant_P,row['r'],F.from_float(w['x']),F.from_float(w['y']),w['exact_coverage'])
            native_witnesses += 1
    require(native_witnesses == 1, 'native_witness_count', 'expected one retained exact native witness')
    crows = [json.loads(line) for line in (ROOT/'exploratory/directions.jsonl').read_text().splitlines()]
    require([row['r'] for row in crows] == list(range(4972)) and all(row['verdict'] == 'VERIFIED' and
            math.isfinite(row['min_bound']) and row['min_bound'] >= 1 for row in crows), 'exploratory_archive', 'incomplete exploratory archive')
    worst = min((row for row,_ in final_rows),key=lambda row:row['min_certified_lower_bound'])
    return dict(status='ARCHIVE_AND_EXACT_AUDIT_PASSED',not_a_fresh_full_net_replay=True,
                certificate_gzip_sha256=CANDIDATE_GZIP,certificate_json_sha256=CANDIDATE_JSON,
                verifier_source_sha256=VERIFIER_SOURCE,directions=4972,range=[0,4971],
                unique=True,finite_bounds_at_least_one=True,min_certified_lower_bound=worst['min_certified_lower_bound'],
                least_bound_direction=worst['r'],sources=source_stats,exact_premises=info,
                native_exact_admission=native_admission,
                listed_rectangle_orbits=853,positive_mass_orbits=len(P['rects']),mass_multiplier='99/100',
                exact_mutant_witness_capture=str(value),exact_mutant_witness_capture_approx=float(value),
                native_exact_witnesses_recomputed=native_witnesses,exploratory_rows_audited=len(crows))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--without-manifest', action='store_true', help='bootstrap only; omit file-manifest checking')
    args = parser.parse_args()
    result = audit(check_manifest=not args.without_manifest)
    text = json.dumps(result,indent=2)+'\n'
    if args.output is not None: args.output.write_text(text)
    print(text,end='')

if __name__ == '__main__':
    try:
        main()
    except PacketError as error:
        print(json.dumps(dict(status='ERROR',code=error.code,detail=error.detail)),file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError, KeyError, TypeError, EOFError, zlib.error, OverflowError) as error:
        print(json.dumps(dict(status='ERROR',code='input_or_io',detail=str(error))),file=sys.stderr)
        sys.exit(1)
