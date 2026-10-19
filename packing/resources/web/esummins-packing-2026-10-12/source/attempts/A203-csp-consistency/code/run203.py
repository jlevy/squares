"""A203 driver: per page, STAGE 0 with the CSP (closed form, <= 30 s per pad) at the g1 pad and at pad 0, the page
docs/residue_map/csp203_<nid>.svg drawn after each pad.  Certificates certs/csp203_<nid>_<pad>_s0.json; results
results/csp203.jsonl (one slim row per (nid, pad); resumable unless --force).
    python run203.py <nid> [--force] [--ud 1] [--step 4]
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.abspath(os.path.join(HERE, "..", "certs"))
RES = os.path.abspath(os.path.join(HERE, "..", "results", "csp203.jsonl"))
sys.path.insert(0, HERE)
import fast30                                                  # noqa: E402
import fig203b as fig203                                       # noqa: E402


def emit(out, cert):
    os.makedirs(os.path.dirname(cert), exist_ok=True)
    json.dump(out, open(cert, "w", encoding="utf-8"), indent=1, default=str)
    slim = {k: v for k, v in out.items() if k not in ("tests", "steps", "rounds", "subrects", "wbox", "free_opts", "alive0", "alive_rects")}
    slim["csp"] = [{k: v for k, v in r.items() if k not in ("unit_rects", "unit_alive", "mask_bits", "dead_units")} for r in out.get("csp") or []]
    slim["cert"] = os.path.relpath(cert, ROOT).replace("\\", "/")
    slim["n_rounds"] = len(out.get("rounds") or [])
    slim["when"] = time.strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(RES), exist_ok=True)
    with open(RES, "a", encoding="utf-8") as f:
        f.write(json.dumps(slim, default=str) + "\n")


def done(nid, pad):
    if not os.path.exists(RES):
        return None
    last = None
    for line in open(RES, encoding="utf-8"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("nid") == nid and d.get("pad") == pad:
            last = d
    return last


def draw(nid):
    try:
        p = fig203.render(nid)
        print("   page: %s" % p, flush=True)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("   fig203 failed: %r" % (e,), flush=True)


def stage0(nid, pad, force, ud, step):
    cert = os.path.join(CERTS, "csp203_%s_%s_s0.json" % (nid, pad))
    prev = done(nid, pad)
    if prev and not force and os.path.exists(cert):
        c = json.load(open(cert, encoding="utf-8"))
        print("   stage 0 %s pad: cached %s" % (pad, c["verdict"]), flush=True)
        return c
    st = fast30.Stage0(nid, pad, ud=ud, sat_step=step)
    out = st.run()
    hh = st.h_hull()
    out["H_hull_raw"] = list(hh) if hh else None
    emit(out, cert)
    rd = out["rounds"][-1] if out["rounds"] else {}
    csp = out["csp"][-1] if out.get("csp") else {}
    print("== stage 0 + CSP %s at the %s pad: %s in %.0f ms; kills %s; CSP: units %s -> %s alive, dead options %d, ms %s; caps %s; forced H %s%s" % (
        nid, pad, out["verdict"], 1000 * out["seconds"], {k: v["kills"] for k, v in out["kills"].items()},
        csp.get("n_units"), csp.get("alive_units"), len(csp.get("dead_opts") or []), csp.get("ms"), out.get("caps"), out.get("forced_H"),
        ("; " + str(out["leaf"])) if out["leaf"] else ""), flush=True)
    draw(nid)
    return out


def belownormal():
    try:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.GetCurrentProcess()
        k.SetPriorityClass(h, 0x00004000)
        k.SetProcessAffinityMask(h, 0xFFFF)
    except Exception:
        pass


if __name__ == "__main__":
    belownormal()
    ap = argparse.ArgumentParser()
    ap.add_argument("nid")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--ud", type=int, default=1)
    ap.add_argument("--step", type=float, default=4.0)
    ap.add_argument("--pads", default="g1,zero")
    a = ap.parse_args()
    for pad in a.pads.split(","):
        stage0(a.nid, pad, a.force, a.ud, a.step)
