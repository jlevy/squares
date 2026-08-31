---
type: is
id: is-01m125gdwa8n0x33b0wj7f7zxn
title: exp-045 declares twelve pre-certificate mutations but the instrument implements eight
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
dependencies: []
created_at: 2026-08-27T17:50:27.201Z
updated_at: 2026-08-28T01:36:55.195Z
closed_at: 2026-08-28T01:36:55.182Z
close_reason: BC-036 complete. Twelve pre-certificate mutations now enforced on twelve distinct failure identifiers, verified by direct call. Four ProofInputs fields added; certificate.acceleration_elimination split into acceleration_correction and acceleration_farkas so each control matches only its own frozen id. The declared twelve was never amended. Exactly four reachable modes existed with no slack, after a call-graph trace cut the grep-derived seven.
resolution: null
duplicate_of: null
---
exp-045's method.control declares 'twelve typed pre-certificate mutations' and its Execution Admission section requires 'all twelve mutations enter before certificate construction and match only their frozen failure identifiers' before any pure -W target run.

cases/n5/minus_w_obstruction.py implements eight and hard-enforces that count:

    if set(mutations) != CONTROL_KEYS or len(mutations) != 8:
        raise ProofInvariantError('control.keys', 'the exact eight-key control set drifted')

CONTROL_KEYS: angle_only_negation_rejected, missing_interior_rejected, missing_owner_rejected, missing_tied_row_rejected, owner3_upper_term_rejected, owner4_width_sign_rejected, realized_sheet_overclaim_rejected, scope_overclaim_rejected.

No other mutation set exists in the lane. minus_w_scale.SCALE_KEYS holds the five scale records (x3 strata = the declared fifteen), not mutations.

The other admission conditions check out: thirteen keyed refusals are present and claim-specific, the accepted angle_sheet / second_order_obstruction / tangent_cones / tangent_inventory helpers are used rather than an exp-043 hand-formula path, and the exp-034 sheet control and exp-036 positive obstruction are wired into the same builder.

This blocks BC-029 target execution. Resolve by building the four missing mutations and raising the enforced count to twelve.

Do NOT resolve by amending the preregistration down from twelve to eight. The criterion was frozen before implementation, and lowering it after seeing what was built is exactly the post-hoc weakening the campaign's admission discipline exists to prevent. If twelve was wrong, that needs an argued amendment recorded as such, not a silent match to the code.
