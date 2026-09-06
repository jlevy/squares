---
type: is
id: is-01m1t1g7fa7gjayw9h0nqpwm9a
title: "main is red: the n=20 doubled-net test names the pointer T-021 moved, so it reads the wrong certificate"
kind: bug
status: open
priority: 0
version: 2
labels: []
dependencies: []
created_at: 2026-09-06T00:22:12.704Z
updated_at: 2026-09-06T00:22:28.937Z
---
Main has been red on the exhaustive tier since PR 83 merged at 663ca37e. Confirmed by run history: run 604 (5ebeb62a, PR 86) succeeded, run 625 (663ca37e, PR 83) failed, run 638 (3f8e1043, PR 88) still fails. PR 88's merge fixed the OTHER half of run 625 -- the stale composite figure record -- so this is now the only thing red.

The failure, from run 638's exhaustive job:

  FAILED tests/test_fractional_interval.py::test_the_retained_n20_certificate_is_accepted_on_the_full_doubled_net
  assert (Fraction(200001, 200000), ...) == (Fraction(50007, 50000), ...)
  1 failed, 52 passed, 2125 deselected in 1809.15s

This is NOT a values question and does not need a research judgment. It is the same pointer bug the same PR already recorded once, three commits earlier: 0dbd4b26 is titled 'records: D-455 -- the 24/5 row named the pointer T-021 moved, so it quoted the wrong atoms'. This is a second instance of it.

packing/cases/n20_fractional_certificate/ holds certificate-24-5.json, certificate-193-40.json and certificate.json, and T-021 moved certificate.json -- the pointer -- to 97/20. The test's load_n20() reads the pointer, so a test written for T-020 now silently loads T-021's certificate and gets its enclosure, 200001/200000 (1.000005), where T-020's is 50007/50000 (1.00014).

Everything about the test says T-020 and nothing says T-021: the docstring opens 'The interval-certified decision of s(19), s(20), s(21) >= 24/5. T-020 stands at C4 on the strength of this route'; the measurements it quotes (5,638,343 boxes, 173 s against the event sweep's 5378 s) are T-020's; and its own last assertion is , which would fail too if the enclosure assertion had not failed first.

The fix is D-455's fix applied to the second site: name certificate-24-5.json explicitly rather than the pointer. Worth checking in the same pass whether any other reader of that case directory takes the pointer when it means a specific rung -- two instances of one mistake in one merge suggests the pointer is easy to reach for by accident.

Worth recording as a defect once fixed, and worth noting for the record: this sat undetected because the exhaustive tier is post-merge only. It is the one tier PR 88 deliberately left out of the pull-request surface, on its measured 1943s cost.

## Notes

One clause was eaten by shell quoting when this bead was created. It should read: and its own last assertion is a check that the certificate's bounded_side equals 24/5, which would fail too if the enclosure assertion had not failed first.
