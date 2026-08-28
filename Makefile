# Markdown formatting for this repository.
#
# Flowmark is the ONLY formatter that owns Markdown here (per its project-setup
# guidance). Do not add Prettier, Biome, or dprint Markdown handling alongside it;
# two Markdown formatters churn each other's output and make hooks nondeterministic.

# Pinned to the latest Rust port of flowmark. The Rust build is the fast one
# (50x+ over the Python reference) and is what we standardise on.
#
# Pinned rather than floating on purpose: an unpinned `uvx --from flowmark-rs`
# re-resolves to whatever is newest on every single run, which is exactly the
# unpinned-zero-install-runner pattern that guidelines/supply-chain-hardening.md
# rule 6 warns against. Bumping this pin is a deliberate, reviewable act.
FLOWMARK := uvx --from flowmark-rs==0.3.2 flowmark

.PHONY: format format-check hooks-install

## Format all Markdown in the repository.
format:
	$(FLOWMARK) --auto .

## Report whether any Markdown would change, without writing. Not wired into CI
## on purpose: formatting drift should never break a build (see lefthook.yml).
format-check:
	$(FLOWMARK) --auto --check .

## Install the git hooks. Run once after cloning.
##
## Pinned for the same reason FLOWMARK is pinned above: an unpinned zero-install
## runner is what `tbd guidelines supply-chain-hardening` rule 6 warns against, and
## it fails in a second way here. On 2026-08-27 the installed hook resolved lefthook
## through a purged npx cache path, so every commit printed "Can't find lefthook in
## PATH" and the format-markdown hook silently did nothing -- while AGENTS.md
## promised that unformatted Markdown could not be committed by accident. 2.1.10 is
## the version verified working here that day.
hooks-install:
	npx lefthook@2.1.10 install

# ---------------------------------------------------------------------------
# Hand-written agent skills.
# ---------------------------------------------------------------------------
#
# Codex reads .agents/skills/, Claude Code reads .claude/skills/. The three
# generated skills (flowmark, softschema, tbd) are written to both by their own
# installers. Hand-written skills have no installer, so .agents/ is the source of
# truth and .claude/ is a mirror kept in step by `make skills-sync`.
#
# List each hand-written skill here. `make skills-check` fails on drift, so a
# skill edited in only one tree is caught rather than silently diverging.
HANDWRITTEN_SKILLS := experiment-loop

.PHONY: skills-sync skills-check check

## Mirror hand-written skills from .agents/skills to .claude/skills.
##
## Plain rm + cp rather than rsync: rsync is not installed in every container this
## repo is worked in (it is absent from the cloud agent image), and a sync target
## that fails on the machine doing the syncing is how the two trees drift. cp -R
## after a clean rm gives the same --delete semantics with only coreutils.
skills-sync:
	@for s in $(HANDWRITTEN_SKILLS); do \
	  rm -rf ".claude/skills/$$s" && mkdir -p ".claude/skills" \
	    && cp -R ".agents/skills/$$s" ".claude/skills/$$s" && echo "synced $$s"; \
	done

## Fail if a hand-written skill differs between the two trees.
skills-check:
	@for s in $(HANDWRITTEN_SKILLS); do \
	  diff -r ".agents/skills/$$s" ".claude/skills/$$s" \
	    || { echo "DRIFT in $$s: run 'make skills-sync'"; exit 1; }; \
	done
	@echo "hand-written skills in sync"

## Everything that should hold before a commit lands. Formatting drift is
## deliberately not included: the pre-commit hook fixes it (see lefthook.yml).
check: skills-check
