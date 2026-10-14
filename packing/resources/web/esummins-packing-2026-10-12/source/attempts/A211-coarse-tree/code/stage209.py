"""A209 -- stage 0 of the chain: A202's closed-form layer + A203's CSP (A203's fast30.Stage0, imported READ-ONLY from
attempts/A203-csp-consistency/code; the page comes through load209.load_page, so a tree record is a page too), <= 30 s
per pad.  A203's / A202's certificates are reused when they exist (the gallery pages); otherwise the certificate is
written here as certs/csp209_<nid>_<pad>_s0.json in A203's format (poly204.load_start reads it through start_of).
A stage-0 DEAD is [C: closed-form trace] (A203's label; no verifier clause)."""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ATT = os.path.join(ROOT, "attempts")
CERTS = os.path.abspath(os.path.join(HERE, "..", "certs"))
sys.path.insert(0, HERE)
import load211 as load209                                     # noqa: E402
load209.install()
import poly204 as P                                            # noqa: E402  (the copy)
_A203 = os.path.join(ATT, "A203-csp-consistency", "code")
if _A203 not in sys.path:
    sys.path.insert(0, _A203)
import fast30 as F30                                           # noqa: E402  READ-ONLY (A203): Stage0 with the CSP


def own_cert(nid, pad):
    return os.path.join(CERTS, "csp209_%s_%s_s0.json" % (nid, pad))


def start_of(nid, pad):
    """A203's / A202's start when it exists (poly204.load_start), else A209's own stage-0 certificate."""
    st = P.load_start(nid, pad)
    if st.get("source"):
        return st
    f = own_cert(nid, pad)
    if not os.path.exists(f):
        return st
    c = json.load(open(f, encoding="utf-8"))
    st = dict(source="A209 csp209 (A203's Stage0 + CSP on the record)", file=os.path.relpath(f, ROOT).replace("\\", "/"), verdict=c.get("verdict"),
              H_box=list(c["roles"]["H"]), forced_H=sorted(c.get("forced_H") or []), role_slots=c.get("role_slots") or {}, units=None, n_units=None, n_units_alive=None)
    csp = c.get("csp") or []
    if csp and csp[-1].get("unit_rects") and csp[-1].get("unit_alive"):
        last = csp[-1]
        keys = [tuple(int(v) for v in k.strip("[]").split(",")) for k in last["unit_rects"]]
        st["units"] = dict(nx=max(k[0] for k in keys) + 1, ny=max(k[1] for k in keys) + 1, nb=max(k[2] for k in keys) + 1, alive=[tuple(u) for u in last["unit_alive"]])
        st["n_units"], st["n_units_alive"] = len(keys), len(last["unit_alive"])
    return st


def stage0(nid, pad, log=print, force=False):
    """-> dict(verdict, leaf, seconds, source, file, kills, caps, forced_H, csp): cached from A203 / A202 / A209, or run now."""
    st = start_of(nid, pad) if not force else dict(source=None)
    if st.get("source"):
        c = json.load(open(os.path.join(ROOT, st["file"]), encoding="utf-8"))
        log("   stage 0 %s pad: %s (%s: %s)" % (pad, c.get("verdict"), st["source"], st["file"]))
        return dict(verdict=c.get("verdict"), leaf=c.get("leaf"), seconds=c.get("seconds"), source=st["source"], file=st["file"], cached=True,
                    kills={k: v.get("kills") for k, v in (c.get("kills") or {}).items()}, caps=c.get("caps"), forced_H=c.get("forced_H"),
                    n_units_alive=st.get("n_units_alive"), n_units=st.get("n_units"), verifier="[C: closed-form trace] A202 stage 0 + A203 CSP (no verifier clause)")
    t0 = time.time()
    s0 = F30.Stage0(nid, pad)
    out = s0.run()
    hh = s0.h_hull()
    out["H_hull_raw"] = list(hh) if hh else None
    f = own_cert(nid, pad)
    os.makedirs(CERTS, exist_ok=True)
    json.dump(out, open(f, "w", encoding="utf-8"), indent=1, default=str)
    csp = out["csp"][-1] if out.get("csp") else {}
    log("== stage 0 + CSP %s at the %s pad: %s in %.0f ms; kills %s; CSP units %s -> %s alive; caps %s; forced H %s%s" % (
        nid, pad, out["verdict"], 1000 * out["seconds"], {k: v["kills"] for k, v in out["kills"].items()}, csp.get("n_units"), csp.get("alive_units"),
        out.get("caps"), out.get("forced_H"), ("; " + str(out["leaf"])) if out.get("leaf") else ""))
    return dict(verdict=out["verdict"], leaf=out.get("leaf"), seconds=round(time.time() - t0, 1), source="A209 csp209 (A203's Stage0 + CSP on the record)",
                file=os.path.relpath(f, ROOT).replace("\\", "/"), cached=False, kills={k: v["kills"] for k, v in out["kills"].items()}, caps=out.get("caps"),
                forced_H=out.get("forced_H"), n_units_alive=csp.get("alive_units"), n_units=csp.get("n_units"),
                verifier="[C: closed-form trace] A202 stage 0 + A203 CSP (no verifier clause)")


if __name__ == "__main__":
    nid = sys.argv[1]
    for pad in (sys.argv[2:] or ["g1", "zero"]):
        r = stage0(nid, pad)
        print(json.dumps({k: r[k] for k in ("verdict", "leaf", "seconds", "source", "file", "n_units_alive")}, default=str))
