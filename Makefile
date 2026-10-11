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
FLOWMARK := uvx --from flowmark-rs==0.4.0 flowmark
PACKING_PYTHON ?= uv run --frozen --group dev python

.PHONY: format format-check paper-style-check hooks-install lint-fix

## Format all Markdown in the repository.
format:
	$(FLOWMARK) --auto .

## Verify canonical paper titles without rendering or writing generated files.
paper-style-check:
	cd packing && $(PACKING_PYTHON) -m devtools.render_overview --check-paper-titles

## Report whether any Markdown would change, without writing. Not wired into CI
## on purpose: formatting drift should never break a build (see lefthook.yml).
format-check:
	$(FLOWMARK) --auto --check .

## Install the browser floor's pinned tools and the git hooks. Run once after cloning.
##
## `npm ci --ignore-scripts` installs exactly what package-lock.json pins -- lefthook,
## the workbench package -- and fails if the lockfile and package.json disagree, which is
## what makes "pinned" mean anything. The hook install then runs the LOCAL lefthook rather
## than fetching one, so the binary that installs the hook is the binary the lockfile
## names.
hooks-install:
	npm ci --ignore-scripts
	./node_modules/.bin/lefthook install

## Fix the JavaScript and CSS floor in place. The verify-only counterpart is a step in
## `packing-validate` and runs on every pull request; this is the local fix command, and
## the commit hook runs the same thing over staged files.
lint-fix:
	./node_modules/.bin/biome check --write --unsafe .

## Run the sweep that starts an intake pass (packing/campaign/result-import.md, Running an
## Intake Pass): capture the Kingbird catalogue into attic/intake/, then list every input
## the record has not taken in, with the bead that owns it or none. It reads the network,
## github.com and kingbird.myphotos.cc. A capture that fails does not stop the sweep, which
## reports the catalogue as not checked. `make intake INTAKE_ARGS=--offline` reads only the
## record, the bead store and the captures already taken.
INTAKE_ARGS ?=
PACKING_MODULE := cd packing && uv run --frozen --all-extras --group dev python -m

.PHONY: intake
intake:
ifeq (,$(findstring --offline,$(INTAKE_ARGS)))
	-$(PACKING_MODULE) devtools.capture_kingbird_catalogue
endif
	$(PACKING_MODULE) devtools.intake_sweep $(INTAKE_ARGS)

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
