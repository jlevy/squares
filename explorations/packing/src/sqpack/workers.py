"""How many processes one parallel step may use.

Several tools here are lists of independent, multi-second quenches, and each one runs
them in a process pool. The gate ALSO runs its steps concurrently, so without a shared
answer to this question the two layers multiply: ten steps, each asking for ten
workers, is a hundred processes on ten cores. Measured on the strict gate, that
oversubscription cost more than the nesting won -- 232s of CPU delivered over 50s of
wall on a ten-core machine, where the steps in isolation were much faster.

The gate exports `PACK_JOBS` as a per-step cap. It is not a cross-process semaphore, so
several simultaneous pool-backed steps can exceed that number in aggregate. A tool run
directly from a shell sees no variable and gets the whole machine, which is what
someone iterating on one file wants.
"""

from __future__ import annotations

import os


def worker_count(units: int) -> int:
    """Workers for a step with `units` independent items of work.

    Never more than there is work to do, never fewer than one.
    """
    requested = os.environ.get("PACK_JOBS")
    if requested:
        try:
            available = int(requested)
        except ValueError:
            available = os.cpu_count() or 4
    else:
        available = os.cpu_count() or 4
    return max(1, min(units, available))
