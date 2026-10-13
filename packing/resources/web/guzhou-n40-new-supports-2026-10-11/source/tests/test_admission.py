"""精确输入与证据拒绝测试；合成记录不是几何证明。
Exact input and evidence-refusal tests; synthetic records are not geometry proofs.
"""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'verifier'))
from exact import *
class Admission(unittest.TestCase):
 def test_inputs(self):
  a,b,r=make_inputs(ROOT/'certificate/certified_candidate.json');self.assertEqual(digest(a),POSE);self.assertEqual(digest(b),AXIS_INPUT)
 def test_scalars(self):self.assertEqual(scalar()['counting_margin'],'1/500')
 def test_false_source(self):
  with self.assertRaises(ValueError):source_rows(ROOT/'certificate/parameters.json')
 def test_duplicate(self):
  with self.assertRaises(ValueError):loads('{"n":40,"n":41}')
 def test_enclosure(self):
  for x in (B,A,L,EPS,LAST,TAU,Q(-1,3),Q(0)):
   a,b=map(float,enclose(x).split());self.assertLessEqual(Q(a),x);self.assertGreaterEqual(Q(b),x)
 def test_slab_refusals(self):
  h='0'*64;rows=[]
  for i,(lo,hi) in enumerate(zip(P['endpoints'],P['endpoints'][1:])):
   r={'status':'verified','pl':lo,'ph':hi,'den':10**6,'nodes':3,'leaves':2,'lower_bound':1.0,'max_depth':1,'angle_splits':1}
   rows.append({'index':i,'arguments':[str(lo),str(hi),'1000000','4999','5000','30000000'],
                'exit_code':0,'timed_out':False,'input_sha256':POSE,'source_sha256':KERNEL,'binary_sha256':h,'stdout':json.dumps(r)})
  self.assertEqual(admit_slabs(rows,h)['slabs'],43)
  tests=[];z=copy.deepcopy(rows);z.pop();tests.append(z)
  for k,v in [('index',1),('arguments',['1','499','1000000','4999','5000','30000000']),('exit_code',3),('timed_out',True),('input_sha256','bad'),('source_sha256','bad'),('binary_sha256','bad')]:
   z=copy.deepcopy(rows);z[0][k]=v;tests.append(z)
  for k,v in [('status','unresolved'),('pl',0),('ph',501),('den',1),('nodes',4),('leaves',0),('lower_bound',0.9997),('lower_bound',float('nan')),('lower_bound',float('inf')),('max_depth',124),('angle_splits',3)]:
   z=copy.deepcopy(rows);r=loads(z[0]['stdout']);r[k]=v;z[0]['stdout']=json.dumps(r);tests.append(z)
  for z in tests:
   with self.assertRaises((ValueError,TypeError,KeyError)):admit_slabs(z,h)
  self.assertEqual(len(tests),19)
 def test_nonfinite_and_nonintegral(self):
  for value in ('NaN','Infinity','-Infinity'):
   with self.assertRaises(ValueError):loads('{"x":'+value+'}')
 def test_axis_refusals(self):
  h='0'*64;r={'status': 'AXIS_COVERAGE_PROVED', 'x_nodes': 3293, 'y_nodes': 3293, 'minimum_numerator': '1001486431423867090847280653', 'scale': '1000000000000000000000000000', 'minimizer_x_integer': 3490012394, 'minimizer_y_integer': 6201340682, 'direct_sum_matches': True, 'evaluation_abs_bound': '627444222088298915573283512797161984'}
  rec={'exit_code':0,'input_sha256':AXIS_INPUT,'source_sha256':AXIS,'binary_sha256':h,'stdout':json.dumps(r)}
  self.assertEqual(admit_axis(rec,h)['vertices'],3293**2)
  for k,v in [('exit_code',3),('input_sha256','bad'),('source_sha256','bad'),('binary_sha256','bad')]:
   z=copy.deepcopy(rec);z[k]=v
   with self.assertRaises(ValueError):admit_axis(z,h)
  for k,v in [('status','AXIS_TEST_REFUSED'),('x_nodes',3292),('direct_sum_matches',False),('scale','1'),('minimum_numerator','0'),('evaluation_abs_bound',str(2**126))]:
   z=copy.deepcopy(rec);rr=copy.deepcopy(r);rr[k]=v;z['stdout']=json.dumps(rr)
   with self.assertRaises(ValueError):admit_axis(z,h)
if __name__=='__main__':unittest.main()
