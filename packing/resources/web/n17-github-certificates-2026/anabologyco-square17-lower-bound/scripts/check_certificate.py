import csv, fractions, json, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
rows=list(csv.DictReader(open(root/'data/atoms.csv')))
assert len(rows)==560
mass=sum(int(r['weight_num']) for r in rows)
expected=16994734834452
assert mass==expected
assert mass<17*10**12
f=fractions.Fraction(mass,10**12)
print('atoms=560')
print('exact_mass='+str(f))
print('mass_decimal='+str(float(f)))
print('slack='+str(fractions.Fraction(17)-f))
print('EXACT CERTIFICATE ARITHMETIC PASS')
