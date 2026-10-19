"""Receipt totals over chosen counts of a packet (reads receipts only, decides nothing)."""
import sys
from devtools import upper_bound_reports as ubr

def totals(name, counts):
    packet = ubr.packet_path(name)
    rows = []
    for p in sorted((packet / "receipts").glob("exact-certification*.json.xz")):
        rows += [r for r in ubr.kernel.read_xz(p)["cases"] if counts is None or r["n"] in counts]
    return ubr.receipt_summary({"cases": rows})

T186 = {129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304}
print("10-11 175", totals("couzo-certificates-2026-10-11", {175}))
print("10-11 other14", totals("couzo-certificates-2026-10-11", {304, 305, 308, 338, 339, 340, 343, 344, 375, 376, 378, 379, 380, 381}))
print("mishapolk 12", totals("mishapolk-kkt-refinements-2026-10-14", T186))
print("mishapolk other12", totals("mishapolk-kkt-refinements-2026-10-14", {153, 155, 181, 207, 209, 267, 270, 272, 305, 306, 307, 308}))
print("607 237", totals("couzo-certificates-2026-10-14", {237}))
print("607 other22", totals("couzo-certificates-2026-10-14", {339, 342, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 703, 757, 804, 812, 930, 931, 992, 993, 994}))
