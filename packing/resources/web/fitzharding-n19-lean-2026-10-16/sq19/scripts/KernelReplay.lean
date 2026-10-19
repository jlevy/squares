import LeanChecker
open Lean

/-- Kernel-replay each listed module with the toolchain's own `replayFromImports`
(LeanChecker, Lean 4.34.1), skipping leanchecker's per-target directory scan.
Prints one OK/FAIL line per module as it finishes. -/
unsafe def checkList (path : String) : IO UInt32 := do
  initSearchPath (← findSysroot)
  let mods := (← IO.FS.lines path).toList.filter (· ≠ "") |>.map String.toName
  let mut tasks := #[]
  for m in mods do
    tasks := tasks.push (m, ← IO.asTask do
      let t ← IO.monoMsNow
      replayFromImports m
      let ms := (← IO.monoMsNow) - t
      IO.println s!"OK {m} {ms}ms"
      (← IO.getStdout).flush)
  let mut bad := 0
  for (m, t) in tasks do
    if let .error e := t.get then
      IO.eprintln s!"FAIL {m}: {e}"; bad := bad + 1
  IO.println s!"DONE modules={mods.length} fail={bad}"
  return if bad == 0 then 0 else 1

unsafe def runFromEnv : IO Unit := do
  let rc ← checkList ((← IO.getEnv "KCHECK_LIST").getD "")
  IO.println s!"RC {rc}"

#eval runFromEnv
