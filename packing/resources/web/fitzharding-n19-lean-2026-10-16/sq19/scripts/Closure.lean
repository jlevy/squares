import Lean
open Lean

/-- Print the full transitive import closure of a module, read from .olean headers. -/
partial def go (m : Name) (seen : IO.Ref NameSet) : IO Unit := do
  if (← seen.get).contains m then return
  seen.modify (·.insert m)
  let f ← findOLean m
  let (md, _) ← readModuleData f
  for i in md.imports do go i.module seen

def main (args : List String) : IO Unit := do
  initSearchPath (← findSysroot)
  let seen ← IO.mkRef ({} : NameSet)
  for a in args do go a.toName seen
  for m in (← seen.get).toList do IO.println m
