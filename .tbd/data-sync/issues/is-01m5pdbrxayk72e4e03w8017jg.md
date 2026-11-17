---
type: is
id: is-01m5pdbrxayk72e4e03w8017jg
title: "Decide: are the Kaggle notebook packings Couzo's 964ee2b index republishes below the record (141 counts at 325-1024, credited to Tymchishin, kyleluecke, alexchilton, aqibrazadev, Lavrentev and others) reports the record takes in?"
kind: task
status: open
priority: 2
version: 1
labels:
  - decision
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T07:35:19.209Z
updated_at: 2026-10-24T07:35:19.209Z
---
Found by c-import-763-1024 while building #763's PR A (think-ptkk), 24 October. At 964ee2b, certified_bounds.json states at 141 counts from 325 to 1024 a bound below main's standing side (the row and Göbel's construction, main 11d0ab06b) that it credits to someone other than Couzo: certificates of public Kaggle 'Squares in Squares' notebook outputs (Kirill Tymchishin 41, kyleluecke 18, alexchilton 11, aqibrazadev 9, Vladislav Lavrentev 8) and constructions (PingYou Ltd 24, Erich Friedman 14, Tymchishin 11, Göbel 4, Lavrentev 1); margins up to 6.6e-2, some (PingYou) only about 2e-23 below. The issue says these 'are retained in our index with their credits and sources, but they are not part of this request'. The triage (think-cnn7) mapped only Couzo-credited rows. By the watched-repository rule each file in franciscouzo/square-packing is a publication from the push that made it public (23:38:42Z), but these are other authors' Kaggle results republished by a third party, whose own licences (Kaggle notebooks) were not read. Question for the owner: are they reports, from which date (the Kaggle run, or the push), credited to whom, and under what licence? Options: (a) take them in as watched publications credited to each notebook's author, after reading each notebook's licence; (b) treat Kaggle as its own intake source and import from the notebooks; (c) do not take them in. Nothing in #763's PR A rests on them: they stand at counts #763 does not claim, after its issue. List: scratchpad import763/recheck/noncouzo.json (n, kind, holder, margin, standing row).
