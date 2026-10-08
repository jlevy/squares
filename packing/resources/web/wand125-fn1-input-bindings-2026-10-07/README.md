# FN-1 Original Input Binding Supplement

[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) at
`b73473fcf60421222b739294d3f7d9c4a8b8da07` supplies the eight exact original gzip files
read by the previously retained check2 runs for n=19,20,26,27,28,30,39,41. The source
manifest and explanation are retained unchanged alongside the MIT licence.
All eleven selected files are acquired with their original Git blobs and SHA-256 values.

The `original_gzip` acquisition contract explicitly retains each compressed file without
renaming or recompression.
Its table below names raw compressed bytes.
The archive’s ordinary Compressed Files table continues to describe decompressed
archived bytes; these two custody contracts remain distinct.

## Binding Scope

The maintained `devtools.wand125_fn1_bindings` command checks the complete eight-input
roster against the original compressed hashes in the existing check2 receipts and
admission tool. Decompression must be byte-for-byte equal to the previously retained
candidate, its decompressed file hash must equal both records, and its mathematical
candidate digest must equal both records.
Every invocation rereads the complete inputs.

This closes original-input byte custody only.
The original check2 native outputs, mathematical certificates, frontier bounds and
assurance ratings stay unchanged.
No geometric verifier or source checker is run by this supplement.
The plain n18=4.705 input and the earlier n18=4.704/n19=4.8229 releases already have
separate retained input bindings and are outside this eight-input supplement.

## Admission and Worker Scope

The retained eight-input command passes the complete original-byte chain.
Its contract and binding controls pass 21 tests, and the existing
acquisition/decompression readers pass 78 regression tests.
Scoped BasedPyright reports zero errors and warnings.

The complete private-worker roster retains all eight original compressed inputs, the
complete eight earlier candidates and receipts, both acquisition records and the binding
manifest. At the measured pre-#432 parent, the maintained source-byte command refused
201,334,850 bytes against the unchanged 201,326,592-byte cap.
That receipt is an early integration observation.
Final private-worker admission and storage acceptance await the #432 parent and the
actual merged snapshot; no input is dropped or linked to make this partial tree fit.

## Retained Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source wand125-fn1-input-bindings-2026-10-07 --check
uv run --frozen --all-extras --group dev python -m devtools.wand125_fn1_bindings
```

## Original Gzip Files

The Git blob and SHA-256 columns bind original compressed upstream bytes, including
their original gzip headers.

| Stored file | Origin | Git blob | SHA-256, raw |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n19_L4825/check2/recorded-input.json.gz` | upstream | `2a5983df6d96da56f76010e2beac265755c27689` | `9132b84eceb4c9913bcf3065be58828665c5b12469c585f1700c1408c7f43cb7` |
| `square-packing-bounds/certificates/mixed_n20_L4905/check2/recorded-input.json.gz` | upstream | `ea535ef37ce1c68845e3085b0af0eb3fa92f5009` | `c446837b499de48ede56a5b3a660abf81615b6332a36314012bca642306cd07f` |
| `square-packing-bounds/certificates/mixed_n26_L5545/check2/recorded-input.json.gz` | upstream | `86ef4bb2003e16a7b0b4528cadf047f1044ce86b` | `6ea9cce160259694f48b9bb5f1ba3222332b7d8051284278f11a4413c6933c95` |
| `square-packing-bounds/certificates/mixed_n27_L56435/check2/recorded-input.json.gz` | upstream | `789fdc30bcf1dc46c7602878c9e3688ceb38eb87` | `e6561fe4d114945a99f81aee05ef3028fb95ee60cf139990e8cd1deffc312dbf` |
| `square-packing-bounds/certificates/mixed_n28_L5735/check2/recorded-input.json.gz` | upstream | `336556b2c419be122a4bb1e4e3f6970608264e51` | `c0218bf04ce2fe50a714cde1a4fe124ec1c90aebc50e5b5d65259cd094522bfd` |
| `square-packing-bounds/certificates/mixed_n30_L58835/check2/recorded-input.json.gz` | upstream | `66370af859d65b1ddd7f4021e0c1660e32d4ecc1` | `6b3d9075e5faa99015409f531c8d3cdc3af69356d9a933e987da5f505ec9d766` |
| `square-packing-bounds/certificates/mixed_n39_L665/check2/recorded-input.json.gz` | upstream | `1266ade4b6a9bdf4ff2f33023d1571e8602a262c` | `012755340a2a7dd214891d3e123ddc29e8dfd6f03c07dccedaf563c02da931ca` |
| `square-packing-bounds/certificates/mixed_n41_L6775/check2/recorded-input.json.gz` | upstream | `b1e02f27b3766ce0b9eff87104b7c282199a69da` | `cbc04bd94c0f7041178419115990eb193ba52a79bc67efa2a2b7d00f8d9588b2` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
