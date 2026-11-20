# Continuing the numerical search

These snapshots retain partial angle searches and their exact candidate measures. The certified results are listed in [best_by_count.csv](../best_by_count.csv). Run `python3 followup/search/resume.py` from the extracted project to list the saved cases, then pass a listed tag and optionally `--workers 4`. The runner compiles the original integer checker with a C++17 compiler and writes intermediate files in a separate working directory. Some candidate measures can fail at a remaining angle.
