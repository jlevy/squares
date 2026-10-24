"""Exact tiling, L-border and deletion consequences of a retained certificate."""
from fractions import Fraction


def derive(source_n, source_side, tiles=1, layers=0):
    if type(tiles) is not int or tiles < 1 or type(layers) is not int or layers < 0:
        raise ValueError('Construction dimensions must be nonnegative integers, with positive tiles')
    count, side = source_n*tiles*tiles, Fraction(source_side)*tiles
    for _ in range(layers):
        count += 2*(side.numerator//side.denominator)+1
        side += 1
    return count, side


def expand(source_rows, source_side, tiles=1, layers=0):
    """Materialize a recipe in rational half-angle coordinates, without search."""
    count, bound = derive(len(source_rows), source_side, tiles, layers)
    side = Fraction(source_side)
    rows = [(x+ix*side, y+iy*side, t) for iy in range(tiles) for ix in range(tiles)
            for x,y,t in source_rows]
    side *= tiles
    half = Fraction(1,2)
    for _ in range(layers):
        k = side.numerator//side.denominator
        rows.extend((side+half, i+half, Fraction(0)) for i in range(k+1))
        rows.extend((i+half, side+half, Fraction(0)) for i in range(k))
        side += 1
    assert len(rows) == count and side == bound
    return rows, bound
