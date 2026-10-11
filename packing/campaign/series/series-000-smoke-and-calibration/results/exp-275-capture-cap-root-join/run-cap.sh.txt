#!/bin/bash
set -e
/Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3 -m devtools.check_n17_capture_cap --output campaign/series/series-000-smoke-and-calibration/results/exp-275-capture-cap-root-join/certificate.json
/Volumes/spud-ext1/agent-scratch/n17-w3-01a114fb/venv/bin/python3 -m devtools.check_n17_capture_cap --certificate campaign/series/series-000-smoke-and-calibration/results/exp-275-capture-cap-root-join/certificate.json --output campaign/series/series-000-smoke-and-calibration/results/exp-275-capture-cap-root-join/replay.json
