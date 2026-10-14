"""A226 -- parse an Ellsworth "Squares in Squares" SVG (kingbird.myphotos.cc/packing/square-N.svg) into unit
squares (cx, cy, theta) in a y-UP frame with the container [0, s]^2, and verify it is a packing.
The SVGs draw flush blocks as merged rectilinear paths on the integer grid of their local frame and tilted
squares as <use href="#one"> / <rect> under nested transforms; entities (&s; &a; ...) hold the numbers.
    from svg226 import load_svg;  sq, s, ents = load_svg(path)      # sq = [(cx, cy, theta_rad), ...]
"""
import math
import re
import xml.etree.ElementTree as ET

import numpy as np

NUM = re.compile(r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')
ENT = re.compile(r'<!ENTITY\s+(\S+)\s+"([^"]*)"')
XLINK = '{http://www.w3.org/1999/xlink}href'


def expand_entities(text):
    ents = dict(ENT.findall(text))
    body = text[text.index('<svg'):]
    for _ in range(8):
        new = re.sub(r'&([A-Za-z0-9_]+);', lambda m: ents.get(m.group(1), m.group(0)), body)
        if new == body:
            break
        body = new
    return body, ents


def parse_transform(s):
    """SVG transform list -> 3x3 matrix (composition left to right)."""
    M = np.eye(3)
    if not s:
        return M
    for name, args in re.findall(r'(\w+)\s*\(([^)]*)\)', s):
        a = [float(x) for x in NUM.findall(args)]
        T = np.eye(3)
        if name == 'translate':
            T[0, 2] = a[0]
            T[1, 2] = a[1] if len(a) > 1 else 0.0
        elif name == 'scale':
            T[0, 0] = a[0]
            T[1, 1] = a[1] if len(a) > 1 else a[0]
        elif name == 'rotate':
            th = math.radians(a[0])
            R = np.array([[math.cos(th), -math.sin(th), 0], [math.sin(th), math.cos(th), 0], [0, 0, 1]])
            if len(a) == 3:
                C = np.eye(3); C[0, 2], C[1, 2] = a[1], a[2]
                Ci = np.eye(3); Ci[0, 2], Ci[1, 2] = -a[1], -a[2]
                R = C @ R @ Ci
            T = R
        elif name == 'matrix':
            T = np.array([[a[0], a[2], a[4]], [a[1], a[3], a[5]], [0, 0, 1]])
        else:
            raise ValueError('transform ' + name)
        M = M @ T
    return M


def path_polygons(d):
    """Parse M/L/H/V/Z (absolute and relative) into closed polygons (list of (x, y) lists)."""
    toks = re.findall(r'[MmLlHhVvZz]|' + NUM.pattern, d)
    polys, cur, pos, cmd, i = [], [], (0.0, 0.0), None, 0
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in 'Zz':
                if len(cur) >= 3:
                    polys.append(cur)
                cur = []
            continue
        if cmd in 'Mm':
            if len(cur) >= 3:
                polys.append(cur)
            x, y = float(t), float(toks[i + 1]); i += 2
            pos = (x, y) if cmd == 'M' else (pos[0] + x, pos[1] + y)
            cur = [pos]; cmd = 'L' if cmd == 'M' else 'l'
        elif cmd in 'Ll':
            x, y = float(t), float(toks[i + 1]); i += 2
            pos = (x, y) if cmd == 'L' else (pos[0] + x, pos[1] + y); cur.append(pos)
        elif cmd in 'Hh':
            x = float(t); i += 1
            pos = (x if cmd == 'H' else pos[0] + x, pos[1]); cur.append(pos)
        elif cmd in 'Vv':
            y = float(t); i += 1
            pos = (pos[0], y if cmd == 'V' else pos[1] + y); cur.append(pos)
        else:
            raise ValueError('path token ' + t)
    if len(cur) >= 3:
        polys.append(cur)
    return polys


def shoelace(poly):
    return 0.5 * abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                         for i in range(len(poly))))


def point_in_poly(p, poly):
    x, y, inside = p[0], p[1], False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def square_inside(x0, y0, poly, tol=1e-9):
    """Is the closed unit square [x0, x0+1] x [y0, y0+1] inside the rectilinear polygon?  Exact: its centre is
    inside and no polygon edge passes through its open interior."""
    if not point_in_poly((x0 + .5, y0 + .5), poly):
        return False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
        if abs(x1 - x2) < tol:                        # vertical edge at x = x1
            if x0 + tol < x1 < x0 + 1 - tol and min(y1, y2) < y0 + 1 - tol and max(y1, y2) > y0 + tol:
                return False
        elif abs(y1 - y2) < tol:                      # horizontal edge at y = y1
            if y0 + tol < y1 < y0 + 1 - tol and min(x1, x2) < x0 + 1 - tol and max(x1, x2) > x0 + tol:
                return False
        else:
            raise ValueError('non-rectilinear polygon edge')
    return True


def cells_of_polygon(poly):
    """Decompose a rectilinear polygon (a union of unit squares whose corners sit at vertex coordinates plus
    integers) into unit cells: candidates from the vertex coordinate lattice, greedy lowest-left, exact inside
    test, count checked against the area.  Returns the cell centres in the local frame."""
    xs, ys = sorted(set(p[0] for p in poly)), sorted(set(p[1] for p in poly))
    area = shoelace(poly)
    span = int(round(max(max(xs) - min(xs), max(ys) - min(ys)))) + 1
    cx = sorted(set(round(x + i, 9) for x in xs for i in range(-span, span + 1)))
    cy = sorted(set(round(y + j, 9) for y in ys for j in range(-span, span + 1)))
    chosen = []
    for y0 in cy:
        for x0 in cx:
            if any(abs(x0 - a) < 1 - 1e-9 and abs(y0 - b) < 1 - 1e-9 for (a, b) in chosen):
                continue
            if square_inside(x0, y0, poly):
                chosen.append((x0, y0))
    if abs(area - len(chosen)) > 1e-6:
        raise ValueError('polygon area %.6f but %d cells' % (area, len(chosen)))
    return [(x0 + .5, y0 + .5) for (x0, y0) in chosen]


def tag(e):
    return e.tag.split('}')[-1]


class Parser:
    def __init__(self, root):
        self.root = root
        self.ids = {e.get('id'): e for e in root.iter() if e.get('id')}
        self.squares = []

    def emit(self, cells, M):
        L = M[:2, :2]
        if abs(abs(np.linalg.det(L)) - 1) > 1e-9 or abs(L[:, 0] @ L[:, 1]) > 1e-9:
            raise ValueError('non-rigid frame ' + str(L))
        th = math.atan2(L[1, 0], L[0, 0])
        for (u, v) in cells:
            p = M @ np.array([u, v, 1.0])
            self.squares.append((float(p[0]), float(p[1]), th))

    def walk(self, e, M):
        style = e.get('style', '')
        if 'fill:none' in style.replace(' ', '') or tag(e) in ('defs', 'script'):
            return
        M = M @ parse_transform(e.get('transform', ''))
        t = tag(e)
        if t in ('svg', 'g'):
            for ch in e:
                self.walk(ch, M)
        elif t == 'use':
            ref = e.get(XLINK, e.get('href', '')).lstrip('#')
            if ref == 'outer':
                return
            T = np.eye(3); T[0, 2], T[1, 2] = float(e.get('x', 0)), float(e.get('y', 0))
            self.walk(self.ids[ref], M @ T)
        elif t == 'rect':
            if e.get('id') == 'outer':
                return
            x, y = float(e.get('x', 0)), float(e.get('y', 0))
            w, h = float(e.get('width')), float(e.get('height'))
            poly = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            self.emit(cells_of_polygon(poly), M)
        elif t == 'path':
            for poly in path_polygons(e.get('d')):
                self.emit(cells_of_polygon(poly), M)
        else:
            raise ValueError('element ' + t)


def load_svg(path):
    text = open(path, encoding='utf-8').read()
    body, ents = expand_entities(text)
    root = ET.fromstring(body)
    s = float(ents['s'])
    P = Parser(root)
    P.walk(root, np.eye(3))
    # SVG y is down: flip to y-up, tilt reflects
    sq = [(x, s - y, (-th) % (math.pi / 2)) for (x, y, th) in P.squares]
    return sq, s, ents


# ---- geometry (exact SAT on convex polygons) --------------------------------------------------------------------
def square_corners(x, y, th):
    c, s_ = math.cos(th), math.sin(th)
    R = np.array([[c, -s_], [s_, c]])
    return np.array([x, y]) + (np.array([(-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5)]) @ R.T)


def sat_overlap(A, B):
    """min over the edge normals of both polygons of the projection overlap (> 0 iff interiors meet)."""
    best = math.inf
    for P in (A, B):
        for i in range(len(P)):
            e = P[(i + 1) % len(P)] - P[i]
            n = np.array([-e[1], e[0]]) / np.hypot(*e)
            a, b = A @ n, B @ n
            best = min(best, min(a.max(), b.max()) - max(a.min(), b.min()))
    return best


def verify_packing(sq, s, tol=1e-9):
    corners = [square_corners(*q) for q in sq]
    for C in corners:
        if C.min() < -tol or C.max() > s + tol:
            raise ValueError('square outside the container')
    gap = math.inf
    for i in range(len(sq)):
        for j in range(i + 1, len(sq)):
            o = sat_overlap(corners[i], corners[j])
            gap = min(gap, -o)
            if o > tol:
                raise ValueError('squares %d, %d overlap by %.3e' % (i, j, o))
    return gap
