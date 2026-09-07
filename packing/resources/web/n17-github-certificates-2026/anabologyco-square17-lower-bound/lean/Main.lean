/-
Benchmark executable: runs the Lean coverage checker over all 148,937
orientation samples and reports timing. This is NOT a proof (use
FullTheorem.lean for that); it exists to measure full-replay feasibility.

  lake exe fullrun            -- all samples
  lake exe fullrun 500        -- first N samples only
-/

import Square17.Basic
import Square17.Checker
import Square17.AtomData
import Square17.SampleDataFull

open Square17

def main (args : List String) : IO Unit := do
  let limit := match args with
    | [n] => (n.toNat?).getD 148937
    | _ => 148937
  let samples := parseSamples sampleFullData
  IO.println s!"atoms={atoms.size} samples={samples.size} running={min limit samples.size}"
  if !(certOK atoms) then
    IO.eprintln "certificate check FAILED"; return
  let t0 ← IO.monoMsNow
  let mut bad : Nat := 0
  let mut done : Nat := 0
  for (p, q) in samples do
    if done >= limit then break
    if !checkSample atoms p q then
      bad := bad + 1
      IO.eprintln s!"FAIL at sample index {done}"
    done := done + 1
    if done % 1000 == 0 then
      let t ← IO.monoMsNow
      IO.println s!"progress {done} elapsed_ms={t - t0}"
  let t1 ← IO.monoMsNow
  IO.println s!"checked={done} failures={bad} elapsed_ms={t1 - t0}"
  IO.println (if bad == 0 then "LEAN COVERAGE REPLAY PASS" else "LEAN COVERAGE REPLAY FAIL")
