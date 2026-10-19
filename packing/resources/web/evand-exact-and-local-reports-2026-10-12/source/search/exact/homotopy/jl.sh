#!/usr/bin/env bash
# Julia (nixpkgs julia-bin) with a project-local depot (.julia, gitignored) and this directory's Project.toml.
#   ./jl.sh script.jl ...      (JULIA_NUM_THREADS defaults to 2: the machine is shared)
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
export JULIA_DEPOT_PATH="$here/.julia" JULIA_PROJECT="$here" JULIA_NUM_THREADS="${JULIA_NUM_THREADS:-2}"
exec nix --extra-experimental-features 'nix-command flakes' shell nixpkgs#julia-bin -c julia "$@"
