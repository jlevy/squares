---
type: is
id: is-01m7p5n85gkfwbqzfk6gavwsch
title: render_announcement credits only the register's source-key finders, so T-319 at 262 reads 'Mykhailo Polkovskyi' though the case credits de Winter, improved by Polkovskyi (think-bx2a)
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
created_at: 2026-11-18T01:52:04.784Z
updated_at: 2026-11-18T05:51:22.202Z
closed_at: 2026-11-18T05:51:22.202Z
close_reason: "Fixed in 57466324a, merged with #1023 (86284ec20, 2026-11-18T05:46Z): render_announcement credits the case record's found_by, improved by improved_by, where the case cites the result's own source; tests at 260, 262, 268 and 292. The #1023 announcement is the tool's output unedited."
resolution: null
duplicate_of: null
---
Found by w3r-pass-1118 on 18 Nov 2026 rendering the announcement for T-310..T-326 (import of #1009). credit_phrase reads credit_parts(credit_text(record)), the bibliography key's line 'Polkovskyi after Ozden, Daniel, Ono, de Winter, ...', shared by all 13 #1009 results; worked_on/refined match only 'refinement of X's packing' headlines, and T-319's headline is "de Winter's packing at 262 improved by Polkovskyi". So the 262 line names Polkovskyi alone, against the owner's answer think-bx2a (found_by de Winter, improved_by Polkovskyi). --lineage names the whole key's chain on every line. Fix: read the case record's found_by/improved_by (or an 'X's packing ... improved by Y' headline) for the line's finders, with a test at 262 (T-319) and 292 (T-323). The PR description of the #1009 import notes the edit for the owner.
