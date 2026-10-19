"""A202 driver: per page, STAGE 0 at the g1 pad and at pad 0 (closed form, <= 30 s each), the page drawn after each;
then STAGE 1 (A200's exact option table on the surviving cells) at the g1 pad and, if alive, at pad 0; the page
redrawn after each.  Certificates certs/f30_<nid>_<pad>_s<stage>.json; results/fast30.jsonl (one slim row per
(nid, pad, stage); resumable: the driver skips a (nid, pad, stage) already present unless --force).
    python run202.py <nid> [--wall 600] [--stage0-only] [--force]
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS = os.path.abspath(os.path.join(HERE, "..", "certs"))
RES = os.path.abspath(os.path.join(HERE, "..", "results", "fast30.jsonl"))
sys.path.insert(0, HERE)
import fast30                                                  # noqa: E402
import fig202                                                  # noqa: E402


def emit(out, cert):
    os.makedirs(os.path.dirname(cert), exist_ok=True)
    json.dump(out, open(cert, "w", encoding="utf-8"), indent=1, default=str)
    slim = {k: v for k, v in out.items() if k not in ("tests", "steps", "rounds", "subrects", "wbox", "free_opts", "alive0")}
    slim["cert"] = os.path.relpath(cert, ROOT).replace("\\", "/")
    slim["n_rounds"] = len(out.get("rounds") or [])
    slim["when"] = time.strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(RES), exist_ok=True)
    with open(RES, "a", encoding="utf-8") as f:
        f.write(json.dumps(slim, default=str) + "\n")


def done(nid, pad, stage):
    if not os.path.exists(RES):
        return None
    last = None
    for line in open(RES, encoding="utf-8"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("nid") == nid and d.get("pad") == pad and int(d.get("stage", -1)) == stage:
            last = d
    return last


def draw(nid):
    try:
        p = fig202.render(nid)
        print("   page: %s" % p, flush=True)
    except Exception as e:
        print("   fig202 failed: %r" % (e,), flush=True)


def stage0(nid, pad, force):
    cert = os.path.join(CERTS, "f30_%s_%s_s0.json" % (nid, pad))
    prev = done(nid, pad, 0)
    if prev and not force and os.path.exists(cert):
        c = json.load(open(cert, encoding="utf-8"))
        print("   stage 0 %s pad: cached %s" % (pad, c["verdict"]), flush=True)
        return c, None
    st = fast30.Stage0(nid, pad)
    out = st.run()
    hh = st.h_hull()
    out["H_hull_raw"] = list(hh) if hh else None
    emit(out, cert)
    rd = out["rounds"][-1] if out["rounds"] else {}
    print("== stage 0 %s at the %s pad: %s in %.0f ms; kills %s; alive cells %s; caps %s; forced H %s%s" % (
        nid, pad, out["verdict"], 1000 * out["seconds"], {k: v["kills"] for k, v in out["kills"].items()},
        {p: len(v) for p, v in (rd.get("single") or {}).items()}, out.get("caps"), out.get("forced_H"),
        ("; " + str(out["leaf"])) if out["leaf"] else ""), flush=True)
    draw(nid)
    return out, st


def hbox_from(out0):
    hh = out0.get("H_hull_raw")
    rec = out0["H_record"]
    if not hh:
        return tuple(rec)
    e = 1e-9
    return (max(hh[0] - e, rec[0]), min(hh[1] + e, rec[1]), max(hh[2] - e, rec[2]), min(hh[3] + e, rec[3]), max(hh[4] - e, rec[4]), min(hh[5] + e, rec[5]))


def alive_from(out0):
    rd = out0["rounds"][-1] if out0["rounds"] else {}
    return {p: [int(c) for c in v] for p, v in (rd.get("single") or {}).items()}


def stage1(nid, pad, out0, wall, force):
    import stage1_202 as S1
    cert = os.path.join(CERTS, "f30_%s_%s_s1.json" % (nid, pad))
    prev = done(nid, pad, 1)
    if prev and not force and os.path.exists(cert):
        print("   stage 1 %s pad: cached %s" % (pad, prev["verdict"]), flush=True)
        return prev
    out, pg = S1.run_stage1(nid, pad, alive_from(out0), hbox_from(out0), wall=wall)
    emit(out, cert)
    draw(nid)
    return out


def belownormal():
    """the lab's process rules: BelowNormal, affinity 0xFFFF (kernel32; no psutil in this interpreter)."""
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
    ap.add_argument("--wall", type=float, default=600)
    ap.add_argument("--stage0-only", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--force-stage0", action="store_true", help="recompute stage 0 (both pads) with the current code; stage 1 stays cached")
    a = ap.parse_args()
    outs = {}
    for pad in ("g1", "zero"):
        outs[pad], _ = stage0(a.nid, pad, a.force or a.force_stage0)
        if outs[pad]["verdict"] == "DEAD" and pad == "g1":
            break
    if a.stage0_only or outs["g1"]["verdict"] == "DEAD":
        sys.exit(0)
    o1 = stage1(a.nid, "g1", outs["g1"], a.wall, a.force)
    if o1["verdict"] == "ALIVE" and outs.get("zero") and outs["zero"]["verdict"] == "ALIVE":
        stage1(a.nid, "zero", outs["zero"], a.wall, a.force)
