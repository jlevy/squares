"""Fresh complete primary replay / 完整主实现重新计算。"""
import json
from pathlib import Path
import numpy as np
from geometry import physical_sites,weight_vectors,build_event_grid,sweep_argmin
from fast_ranges import feasible_y_ranges_fast

CTX=None


def initialize(candidate):
    global CTX
    cert=json.loads(Path(candidate).read_text(encoding='utf-8'))
    sites,owners=physical_sites(cert)
    CTX=cert,sites,owners,weight_vectors(cert,None)


def row_minimum(row):
    cert,sites,owners,weights=CTX
    grid=build_event_grid(cert,row,sites,owners,weights)
    first,last=feasible_y_ranges_fast(grid)
    events,atoms=grid['events'],grid['atoms']
    arrays=(len(grid['y_events'])-1,
        *[np.array([e[i] for e in events],dtype=np.int64) for i in range(3)],
        np.array(grid['ylo'],dtype=np.int64),np.array(grid['yhi'],dtype=np.int64),
        np.array([w for _,w in atoms],dtype=np.int64),np.array(first,dtype=np.int64),np.array(last,dtype=np.int64))
    minimum,ix,iy,cells=sweep_argmin(*arrays)
    if ix<0 or iy<0:raise ValueError('No legal cell / 没有合法胞元')
    return dict(row=row,minimum_units=int(minimum),cells=int(cells),slabs=sum(a>=0 for a in first))
