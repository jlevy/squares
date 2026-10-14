---
type: is
id: is-01m4ycpqezk8hdbpr0h7x5d8f2
title: "Follow-ups from #608's review: never call a sample confirmed (check_requests), #600 follow-up, remaining ry-xu credits, sample citation rule"
kind: task
status: open
priority: 1
version: 1
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
created_at: 2026-10-14T23:42:03.230Z
updated_at: 2026-10-14T23:42:03.230Z
---
From the senior review of #608 (approved, merged 0dd9003e0).

S1, before posting the #600 follow-up: packing/devtools/check_requests.py:315 _evidence_entry labels any passed replay 'confirmed', samples included. epistemics.md:244 says a sample is never called confirmed. Fix: when independence.coverage.extent == 'sample', state 'recorded' or 'reviewed' with 'sampled, k of N unit'. Then mark the posted #600 reply 6179773241's statements outdated in result-requests.yaml: 'E-wand125-closed-form-cfcheck-sample (confirmed)', and 'V0 because no record has been replayed here', which T-180 now makes untrue. Then post the #600 follow-up (think-tsox) correcting both and naming E-wand125-closed-form-replay4d-sample with the ~5,250 CPU-h price.

S2, the owner's policy call: epistemics.md:262-263 says a sample is cited by the case record, not the result. T-180 cites cfcheck-sample and replay4d-sample from the result, with deferrals that will never clear. Proposal: one epistemics sentence saying a sample that decides no count is cited by its result, which check_results does not count; exempt extent: sample in check_certificate_citations; drop both deferrals in certificate-citation-deferrals.yaml.

S3, remaining handle credits:
- register_ryxu_reports.py:508 still writes 'Credit to ry-xu';
- build_known_best_atlas.py:1291 writes 'ry-xu, <url>' into resources/web/known-best-packings/sources.json;
- register_gupta_reports.py:579 and source-coverage.yaml (about lines 7060-7095 and 7222-7234) say 'ry-xu construction';
- result-requests.yaml (about 6494-6503 and 6562) says 'ry-xu's design' and 'ry-xu's packing'.
Use FINDER, 'Xu construction' and 'Ryan Xu's', then regenerate.

Nits:
- N1: release.py:92 and :688 should read 'the News entries for #602 and #605', not '13 and 14 October', at the next site cut.
- N2: adopt_houses FORMER_NAME_FIELD rewrites only the first list item.
- N3: add 'Ryan Xu (ry-xu)' to credited_names, after the Chaoweeraprasit (itsnaka) pattern.
- N4: #593's follow-up record lists other-70, which the comment does not mention.
- N5: T-180 and its evidence say 'the two smallest records'; they are the cheapest by CPU, not the smallest by leaves.
- N6: check_requests compares issue comments only, not PR reviews; say so in its docstring.

Order: the S1 code fix can go first on its own (check_requests.py and its test only). The data parts (result-requests, source-coverage, results text, bibliography) should follow the other coordinator's next records PR, which touches the same files.
