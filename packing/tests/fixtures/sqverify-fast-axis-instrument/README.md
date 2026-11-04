# The Axis Sweep’s Upper End, Instrumented

`axis-value-hi.patch` is the instrumentation behind the upper ends that
`tests/test_sqverify_fast_axis.py` pins in `CRATE_UPPER`. `sqverify-fast` reports only
the lower end `l` of the interval its axis vertex sweep holds at its least vertex.
This patch, applied to the reviewed crate source `d97758bb…`, also records `value.hi`
where `min_lower` is set and prints both ends to standard error.
`devtools.sqverify_fast_axis` walks the same column in Python.
Its upper end `u'` is tied to the crate only through these values (that module’s
docstring says why), so the patch is kept here and anyone can reproduce the pins.

It is never applied in the tree: any change under `packing/sqverify_fast/src/` is a new
`source_sha256`, and a census row is admitted only from reviewed source.
To reproduce, from the repository root:

```bash
work=$(mktemp -d)
cp -r packing/sqverify_fast "$work/" && rm -rf "$work/sqverify_fast/target"
patch -d "$work" -p2 < packing/tests/fixtures/sqverify-fast-axis-instrument/axis-value-hi.patch
(cd "$work/sqverify_fast" && cargo build --release --locked)   # rustc 1.98.0, its toolchain file
"$work/sqverify_fast/target/release/sqverify-fast" --candidate CANDIDATE --n N \
  --directions 0 --confirm 2>&1 | grep INSTRUMENT
```

`CANDIDATE` is the census case’s retained candidate, or its 99/100 mutant as the census
control writes it
(`devtools.sqverify_fast_census.mixed_mutant(raw, factor=CONTROL_SCALE)`, JSON). The
printed `lo` must equal the census row’s or the control receipt’s axis bound, and `hi`
the pinned value. It was run this way on 4 November 2026 (intake lane L37), with a
28-second build:

- `mixed_n37_L64975`: original `hi=1.002369279185975`, mutant `hi=0.9923455863941246`;
- `mixed_n94_L9965`: original `hi=1.0031171867987096`, mutant `hi=0.9930860149308234`.

The lower ends and argmins equaled the reviewed build’s. Review A of #892 had reported
s(37)’s values and s(94)’s mutant value from its own equivalent build, and #898’s senior
review reproduced s(94)’s two with its own three-line patch.
`tests/test_sqverify_fast_axis.py` checks that the patch’s context still matches the
crate’s `axis.rs`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
