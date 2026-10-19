"""solve_proj.jl output -> filter.jl input ("N|S F re im ..."), skipping failed paths and points with some t_i = inf."""
import sys
n = {'N': 0, 'S': 0, 'X': 0, 'inf': 0}
with open(sys.argv[2], 'w') as out:
    for l in open(sys.argv[1]):
        f = l.split()
        if f[0] == 'X':
            n['X'] += 1; continue
        minb = float(f[2].split('=')[1])
        if minb < 1e-12:
            n['inf'] += 1; continue
        n[f[0]] += 1
        out.write(f[0] + ' F ' + ' '.join(f[4:]) + '\n')
print(n)
