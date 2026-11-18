"""The pricing trial of the review of jlevy/squares#1031 (decides nothing).

Run in scratch before the checker's freeze, on a synthetic packing of 299 squares with
84-digit centre denominators, as `python -I -B rv1031_price.py PROGRAMS_DIR`; kept here
unchanged but for this docstring. It printed: `A 1.1 B 2.1 cmp 0.0`, all 44,551 pairs
apart, `contract 1.5`, and 0.142 ms a pair for the corner projections.
"""
import sys, time, random
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1])
import rv1031_reader as R, rv1031_decide as D, rv1031_contract as K
rng = random.Random(7)
E = 5 * 10**83
poses = []
# a 17 x 17 grid of upright squares at pitch 1 + tiny, plus 10 tilted ones in free space; big denominators
for i in range(17):
    for j in range(17):
        poses.append((F(2*i+1, 2) * (1 + F(1, 10**28)) + F(rng.randint(0, 10**20), E), F(2*j+1, 2) * (1 + F(1, 10**28)) + F(rng.randint(0, 10**20), E), F(1), F(0)))
for k in range(10):
    t = F(rng.randint(1, 10**80), 10**80)
    ux, uy = R.tangent_direction(t)
    poses.append((F(30 + 2*k) + F(rng.randint(0, 10**60), E), F(30), ux, uy))
side = F(60)
print(len(poses))
t0 = time.process_time(); da = D.decide_a(poses, side); t1 = time.process_time()
corners = [R.pose_corners(p) for p in poses]
db = D.decide_b(corners, side); t2 = time.process_time()
cmp_ = D.compare(da, db); t3 = time.process_time()
print('A', round(t1-t0,1), 'B', round(t2-t1,1), 'cmp', round(t3-t2,1), D.summarize_a(da, side)['classes'])
t4 = time.process_time(); rec = K.contraction(poses, side, verify=False); print('contract', round(time.process_time()-t4,1), rec['contraction_margin_short'])
import rv1031_axes as A
t5 = time.process_time()
n=0
for i in range(len(poses)):
    for j in range(i+1, min(len(poses), i+40)):
        A.corner_projection_margin(corners[i], corners[j]); n+=1
print('cp per pair ms', round((time.process_time()-t5)/n*1000,3))
