# Third-party notices

## tokoharu/square-packing-density-bounds

`solver/` contains files from <https://github.com/tokoharu/square-packing-density-bounds>
(commit `84bebef51856d46a19c145b035664324ba9572d3`), unchanged or modified as listed in
`solver/PROVENANCE.md`.

```
MIT License

Copyright (c) 2026 tokoharu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## evand/square-packing

`performance/point_verifier_lazy/lazy-endpoints.patch` is a patch against
`s12/verify2/src/bin/zmx2.rs` of <https://github.com/evand/square-packing>
(commit `6e1223cf7ef2be4c70baaa36c0e7e7197076735a`); its context lines reproduce parts of that file.

```
MIT License

Copyright (c) 2026 Evan Daniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## jlevy/squares

`fine_net_verifier/sqverify_fast/`, `fine_net_witnesses/sqverify_fast_witnesses/` and
`sqverify_continuous/sqverify_fast/` contain
`packing/sqverify_fast` of <https://github.com/jlevy/squares> (base commit
`dee22b882499a295b05424ca5a25121195259ebf`), modified as listed in each directory's
PROVENANCE.md. Its code is under the MIT License below. Its documentation in those
directories (`README.md`, `SOUNDNESS.md`, `INDEPENDENCE.md`, `independence-record.yaml`)
is under Creative Commons Attribution 4.0 International
(<https://creativecommons.org/licenses/by/4.0/>): "Joshua Levy, the squares project
(https://github.com/jlevy/squares)"; our changes to `README.md` and `SOUNDNESS.md` are
listed in PROVENANCE.md.

`n17_bb_verifier/tests/cells.json` (the capacity-one cover), `n17_bb_verifier/tests/fixtures/small-certificate`
(written by the project's branch-and-bound pilot) and the `mutated-*` copies derived from it come from
<https://github.com/jlevy/squares> and are used under the same MIT License below. The verifier's code in
`n17_bb_verifier/` is ours (MIT, `n17_bb_verifier/LICENSE`).

`n17_kernel_verifier/` is a Rust port of `packing/devtools/verify_n17_kernel_certificate.py`
of <https://github.com/jlevy/squares> (commit `ef79288a4`), under the MIT License below; its
test fixture `tests/data/stall-w7-bins8/` is from that repository's campaign record, under
CC BY 4.0 as described above for the documentation of `sqverify_fast`. See `n17_kernel_verifier/PROVENANCE.md`.

```
MIT License

Copyright (c) 2026 Joshua Levy

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
