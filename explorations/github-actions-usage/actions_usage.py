#!/usr/bin/env python3
"""Reconstruct GitHub Actions billing per repo from workflow-run and job data.

Useful when you don't have a `user`-scoped token for the billing API
(`/users/{user}/settings/billing/usage`). Uses `gh api` for auth, so any
token with `repo` scope works. Billing arithmetic matches GitHub's meter for
standard hosted runners: each job rounds up to the whole minute, then an OS
multiplier applies (Linux 1x, Windows 2x, macOS 10x). Only private repos
consume paid minutes on standard runners; public repos are checked anyway so
you can spot paid larger runners by label.

Usage:
    ./actions_usage.py --owner jlevy --since 2026-07-01 --until 2026-08-22

Results are cached under --workdir (default .cache/), so reruns are cheap and
interrupted scans resume. Typical cost: one API call per repo plus one per
run in the window; check with `gh api /rate_limit` if scanning many repos.
"""

import argparse
import collections
import datetime as dt
import json
import math
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

MULT = {"linux": 1, "windows": 2, "macos": 10}
PRICE = {"linux": 0.008, "windows": 0.016, "macos": 0.08}  # standard PAYG $/min
RUN_FIELDS = ["id", "name", "path", "event", "status", "conclusion",
              "created_at", "run_started_at", "updated_at", "run_attempt"]


def gh_api(url, retries=4):
    for attempt in range(retries):
        p = subprocess.run(["gh", "api", url], capture_output=True, text=True)
        if p.returncode == 0:
            return json.loads(p.stdout)
        err = (p.stderr or p.stdout).strip()
        if "HTTP 404" in err or "Not Found" in err:
            return None
        if attempt == retries - 1:
            raise RuntimeError(f"{url}: {err[:200]}")
        time.sleep(2 * (attempt + 1))


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def os_of(labels):
    joined = " ".join(labels or []).lower()
    if "macos" in joined:
        return "macos"
    if "windows" in joined:
        return "windows"
    return "linux"


def list_repos(owner):
    p = subprocess.run(
        ["gh", "repo", "list", owner, "--limit", "1000",
         "--json", "name,isPrivate,isArchived"],
        capture_output=True, text=True, check=True)
    return json.loads(p.stdout)


def fetch_runs(owner, repo, start, end, out):
    """Collect runs created in [start, end], splitting the window when a
    query would exceed the API's 1000-results-per-query cap."""
    base = (f"/repos/{owner}/{repo}/actions/runs?per_page=100"
            f"&created={start.isoformat()}..{end.isoformat()}")
    first = gh_api(base + "&page=1")
    if first is None:
        return
    total = first.get("total_count", 0)
    if total == 0:
        return
    if total > 1000 and start < end:
        mid = start + (end - start) // 2
        fetch_runs(owner, repo, start, mid, out)
        fetch_runs(owner, repo, mid + dt.timedelta(days=1), end, out)
        return
    runs = first.get("workflow_runs", [])
    page = 2
    while len(runs) < total and page <= 10:
        data = gh_api(base + f"&page={page}")
        batch = (data or {}).get("workflow_runs", [])
        if not batch:
            break
        runs.extend(batch)
        page += 1
    for r in runs:
        rec = {k: r.get(k) for k in RUN_FIELDS}
        rec["repo"] = repo
        out.append(rec)


def fetch_jobs(owner, repo, run_id, jobs_dir):
    out_path = os.path.join(jobs_dir, f"{repo}-{run_id}.json")
    if os.path.exists(out_path):
        return
    jobs, page = [], 1
    while True:
        d = gh_api(f"/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
                   f"?per_page=100&page={page}")
        batch = (d or {}).get("jobs", [])
        jobs.extend({k: j.get(k) for k in
                     ("name", "labels", "started_at", "completed_at",
                      "conclusion", "workflow_name")} for j in batch)
        if len(batch) < 100:
            break
        page += 1
    tmp = out_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump({"repo": repo, "run_id": run_id, "jobs": jobs}, f)
    os.replace(tmp, out_path)


def scan(owner, start, end, workdir, jobs_for_public):
    runs_dir = os.path.join(workdir, "runs")
    jobs_dir = os.path.join(workdir, "jobs")
    os.makedirs(runs_dir, exist_ok=True)
    os.makedirs(jobs_dir, exist_ok=True)

    repos = list_repos(owner)
    with open(os.path.join(workdir, "repos.json"), "w") as f:
        json.dump(repos, f)
    private = {r["name"] for r in repos if r["isPrivate"]}

    def scan_repo(repo):
        out_path = os.path.join(runs_dir, f"{repo}.jsonl")
        if os.path.exists(out_path):
            with open(out_path) as f:
                return [json.loads(line) for line in f]
        out = []
        fetch_runs(owner, repo, start, end, out)
        tmp = out_path + ".tmp"
        with open(tmp, "w") as f:
            for rec in out:
                f.write(json.dumps(rec) + "\n")
        os.replace(tmp, out_path)
        return out

    all_runs = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(scan_repo, r["name"]): r["name"] for r in repos}
        for i, fut in enumerate(as_completed(futs), 1):
            runs = fut.result()
            all_runs.extend(runs)
            if runs:
                print(f"[{i}/{len(repos)}] {futs[fut]}: {len(runs)} runs")

    # Job detail for every private-repo run (billable), plus a sample of the
    # longest public-repo runs to catch paid larger runners by label.
    tasks = []
    by_repo = collections.defaultdict(list)
    for r in all_runs:
        by_repo[r["repo"]].append(r)
    for repo, runs in by_repo.items():
        if repo in private:
            tasks += [(repo, r["id"]) for r in runs]
        else:
            runs = sorted(runs, key=lambda r: r.get("updated_at") or "",
                          reverse=True)
            tasks += [(repo, r["id"]) for r in runs[:jobs_for_public]]
    print(f"fetching job detail for {len(tasks)} runs")
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(fetch_jobs, owner, repo, rid, jobs_dir)
                for repo, rid in tasks]
        for fut in as_completed(futs):
            fut.result()
    return repos, all_runs


def report(workdir):
    repos = json.load(open(os.path.join(workdir, "repos.json")))
    private = {r["name"] for r in repos if r["isPrivate"]}
    runs_meta = {}
    runs_dir = os.path.join(workdir, "runs")
    for fn in os.listdir(runs_dir):
        if not fn.endswith(".jsonl"):
            continue
        with open(os.path.join(runs_dir, fn)) as f:
            for line in f:
                r = json.loads(line)
                runs_meta[(r["repo"], r["id"])] = r

    Agg = lambda: {"quota": 0.0, "usd": 0.0, "raw": collections.Counter(),
                   "months": collections.Counter(),
                   "jobs": collections.Counter(),
                   "labels": collections.Counter()}
    agg = collections.defaultdict(Agg)
    jobs_dir = os.path.join(workdir, "jobs")
    for fn in os.listdir(jobs_dir):
        if not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(jobs_dir, fn)))
        repo = d["repo"]
        meta = runs_meta.get((repo, d["run_id"]), {})
        month = meta.get("created_at", "")[:7]
        for j in d["jobs"]:
            if not (j.get("started_at") and j.get("completed_at")):
                continue
            sec = (ts(j["completed_at"]) - ts(j["started_at"])).total_seconds()
            if sec <= 0:
                continue
            runner_os = os_of(j.get("labels"))
            mins = math.ceil(sec / 60)
            a = agg[repo]
            a["raw"][runner_os] += mins
            a["quota"] += mins * MULT[runner_os]
            a["usd"] += mins * PRICE[runner_os]
            a["months"][month] += mins * MULT[runner_os]
            a["jobs"][(j.get("name") or "?")[:60]] += mins * MULT[runner_os]
            a["labels"][",".join(j.get("labels") or [])] += 1

    print("\n=== Billable quota-minutes (private repos, standard runners) ===")
    print(f"{'repo':24} {'quota-min':>10} {'est USD':>9}   by month / by OS")
    total_q = total_usd = 0.0
    billable = [(r, a) for r, a in agg.items() if r in private and a["quota"]]
    for repo, a in sorted(billable, key=lambda kv: -kv[1]["quota"]):
        total_q += a["quota"]
        total_usd += a["usd"]
        months = " ".join(f"{m}:{q:.0f}" for m, q in sorted(a["months"].items()))
        oses = " ".join(f"{o}:{m}" for o, m in a["raw"].most_common())
        print(f"{repo:24} {a['quota']:10.0f} {a['usd']:9.2f}   {months} / {oses}")
    print(f"{'TOTAL':24} {total_q:10.0f} {total_usd:9.2f}")

    for repo, a in sorted(billable, key=lambda kv: -kv[1]["quota"])[:3]:
        print(f"\n--- {repo}: top jobs by quota-minutes ---")
        for name, q in a["jobs"].most_common(10):
            print(f"  {q:8.0f}  {name}")

    print("\n=== Runner labels in sampled public-repo jobs ===")
    print("(anything beyond ubuntu/windows/macos-latest may be a paid larger runner)")
    for repo, a in sorted(agg.items()):
        if repo in private or not a["labels"]:
            continue
        labels = "; ".join(f"{k or '<none>'}x{v}"
                           for k, v in a["labels"].most_common(4))
        print(f"  {repo:24} {labels}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--owner", required=True)
    ap.add_argument("--since", required=True, help="YYYY-MM-DD")
    ap.add_argument("--until", default=dt.date.today().isoformat())
    ap.add_argument("--workdir", default=".cache")
    ap.add_argument("--jobs-for-public", type=int, default=8,
                    help="longest public-repo runs per repo to label-check")
    ap.add_argument("--report-only", action="store_true",
                    help="skip scanning; summarize existing workdir")
    args = ap.parse_args()
    if not args.report_only:
        scan(args.owner, dt.date.fromisoformat(args.since),
             dt.date.fromisoformat(args.until), args.workdir,
             args.jobs_for_public)
    report(args.workdir)


if __name__ == "__main__":
    main()
