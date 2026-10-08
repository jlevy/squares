import Lake
open Lake DSL

package elevenSquare where
  moreLeanArgs := #["-DautoImplicit=false", "-DmaxHeartbeats=0", "-s65536"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"

@[default_target]
lean_lib ElevenSquare

-- Independent certificate checker imported from wand125 / evand.
lean_lib Sqpack where
  moreLeanArgs := #["-DautoImplicit=true"]
