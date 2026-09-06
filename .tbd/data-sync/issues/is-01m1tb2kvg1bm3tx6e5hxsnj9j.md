---
type: is
id: is-01m1tb2kvg1bm3tx6e5hxsnj9j
title: A merge can revert the kpress pointer backwards and no gate objects
kind: bug
status: open
priority: 2
version: 1
labels:
  - tooling
dependencies: []
created_at: 2026-09-06T03:09:32.396Z
updated_at: 2026-09-06T03:09:32.396Z
---
`vendor/kpress` was reverted from `3eada69` to `1c0bdb6d` by a merge, undoing a
deliberate bump, and nothing anywhere noticed.

## What happened

`0d57a942` took kpress `3eada69` — the print block-gutter fix, worth a page off the
printed explainer — and PR #88 put it on main at `3f8e1043`. PR #87's branch predated
that commit and recorded `1c0bdb6d`. Its merge at `57135eec` resolved the submodule to
the older one, and main has carried the revert since. Merging main into a branch
propagates it.

A submodule pointer moving backwards is a well-formed one-line diff. Git does not treat
it as a conflict when one side simply has an older value, and no check in this repository
reads the pointer at all.

## Why it stayed invisible locally

A submodule's *recorded* commit and its *checked-out* commit are different things. A
working tree that has been on `3eada69` for hours keeps rendering against `3eada69` no
matter what the index says, so every local render, PDF and print check was correct while
the committed state was not. CI checks out what is recorded, which is the only place the
difference shows — and it shows as output that merely looks different rather than wrong:
the CI PDF is 892,061 bytes against this machine's 979,792 for the same page count, a gap
that reads as a host-font difference until you look.

## The check that would catch it

A merge may only move a submodule pointer to a descendant of what the base recorded.
Cheap to state and cheap to run:

    git -C vendor/kpress merge-base --is-ancestor <recorded-before> <recorded-after>

Run it against the merge base rather than against either parent, so a genuine downgrade
can still be made deliberately by saying so, and an accidental one fails. Worth applying
to every submodule the repository gains, not just kpress.

Related: the render's `RENDER_INPUTS` already names `REPO / "vendor" / "kpress"` as an
input the Pages filter must cover, so the pointer is understood to matter — it just is
not checked for direction.
