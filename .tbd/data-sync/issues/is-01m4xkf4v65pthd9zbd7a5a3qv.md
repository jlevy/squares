---
type: is
id: is-01m4xkf4v65pthd9zbd7a5a3qv
title: Redesign CI around a three-minute default gate and explicit deeper validation
kind: feature
status: in_progress
priority: 1
version: 27
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
child_order_hints:
  - is-01m4xkmdn3wbb62yx8wjtc5ec4
  - is-01m4y1bk4xqtpbjc6ppar1abj7
  - is-01m4y1d2r15w1pc4xpakvwaqfn
  - is-01m4y3k8x8386gz568dw7fb138
  - is-01m4y4hnnycgs1408k8xdd50bb
  - is-01m4y4hp4ewatvtj8bprsb39v7
  - is-01m4y6atnwkc1mnv7wdb1rp9f8
  - is-01m4y6k1fydknqmakgxgtemj1a
  - is-01m4yamkb10vnaryngp4tcp5kb
  - is-01m4ybb1t86fyv3t8mr0j08dk9
  - is-01m4yby40b4wk2yevnnphcrkmp
  - is-01m4yc9h8wqsdkyzc7j4kggjh6
  - is-01m4yckgfyh5xam1qjmbfgkz98
  - is-01m4yckgxyr9fbtzhwjbyj085f
  - is-01m4yckhbnm40kj2r6dyd4vybh
  - is-01m4ydp69m2z8v6c75mgngwbvy
  - is-01m4zhkc4z66ywdsxw20sjcmg7
  - is-01m4zq0njqcj232mhnhc0nwfa3
  - is-01m4zxh554nzhg3eveyxbw75sw
  - is-01m504m9vnya2jnvwddcsjbttp
  - is-01m50p364zjg93qw5e3vt6ggvd
  - is-01m51nbp3q902wgcm3fw09kfwd
hold: null
hold_until: null
created_at: 2026-10-14T16:21:00.389Z
updated_at: 2026-10-16T06:11:01.878Z
started_at: 2026-10-14T16:21:26.412Z
---
User explicitly requests Astra analysis and a systematic fix for repeated hours of CI iterations. Target typical default PR CI around three minutes; retain expensive tests in clearly selected deeper, checkpoint or scheduled lanes without blocking every development iteration. Audit actual validation/workflow costs, require each addition to account for recurring forward cost, define affected-input selection and evidence reuse with fail-closed assurance, document clear running policy and implement reviewed slices. Current PR599 timing repairs and atlas-width delivery continue separately.

## Notes

2026-10-15 final-head follow-up: Additional cost lesson from final PR620: coordinator-selected effective PythonCPUs2/jobs2/inner1 made the whole quick prepush artificially low-throughput (one pytest worker):67 prerequisites passed but broad suite only~23% in800.4s. Root interrupted rather than silently rerunning or counting it green; retained outputs and process exit130 document the decision. Hosted matching-head complete run38756833833 now owns the remaining coverage with native intended allocation. The one-worker native split adds one browser bootstrap rather than four; full-host measurement and three-minute objective remain open. This interval is distinct from source implementation, billed compute, and the prior failed40m17s full job.

2026-10-15T16:01:14.472296+00:00: Astra next-slice diagnosis is tracked concretely as think-nqnx: ordinary frontend540s includes426.51s layout plus106ssetup; no extra job fixes the tail. Candidate is invocation-local canonical fixture preparation, pending cold-render profiling and predeclared3alternating inclusive trials with >=30s AND10percent improvement, no addedresources/skips/changedoutcomes. It is not measured/accepted. Final620 local six-file correction still selected126files and took662.57s, so selector/fixture cost remains material; three-minute target is OPEN. Source43 is frozen and hosted checkpoint runs while assurance repairs proceed.
