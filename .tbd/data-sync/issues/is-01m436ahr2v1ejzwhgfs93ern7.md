---
type: is
id: is-01m436ahr2v1ejzwhgfs93ern7
title: Bounded least-supported-owner scheduling from accepted enhanced supports
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
assignee: guzhou0806-codex-t0
delegate: codex@guzhou
labels: []
dependencies: []
parent_id: is-01m42d0zw28532d573ersbnzh4
hold: null
hold_until: null
created_at: 2026-10-04T10:11:03.041Z
updated_at: 2026-10-04T10:44:44.217Z
started_at: 2026-10-04T10:11:04.956Z
closed_at: 2026-10-04T10:44:44.216Z
close_reason: ONE frozen target plus independent660pair replay accepted60/96 parents(+19),36unknown; final1b534 source and metadata allrequiredCI green; no negative or causal scheduling claim.
resolution: null
duplicate_of: null
---
# P02B：单次 least-supported-owner 调度

Guzhou六小时授权08:36:46Z–14:36:46Z，root W3设计GO；A已真实交付，final0dcc
19pass/36skip/all3requiredSUCCESS，think-wh57已closed/synced。唯一primary/integrator
graph_gate Sol6.1；root只拥有control/P02B_COORDINATOR_REVIEW.md与runs/p02b-independent-*，
源码关键gate和独立回放。无额外agents或并行实现者。

Actualstart2026-10-04T10:10:14.903951+00:00，source/control30min deadline2026-10-04T10:40:14.903951+00:00；
checkpoint20min2026-10-04T10:30:14.903951+00:00；项目90min deadline2026-10-04T11:40:14.903951+00:00，
15min finalreserve始于2026-10-04T11:25:14.903951+00:00。全窗口30min finalreserve14:06:46Z保持，
无source/clock/cap ladder。Entry research-loop/correctness，经review-planning-oversight。

输入/归属：ownDraft333/guzhou/n17-residual-compatibility baseline0dcc3d6e8ec7f675fb12ad122fd9250a97b2f2f3；
actualfetch main225d6b5e224e3acd5fab48af71cd698450d3f08b/parent3071525d4e03b891d6cbc9a7c0bb3fd1880765cfb65，无相关重叠。
live scopedownership仅own67ek，adaptiveK2ljxn/capture/Flag2不动；session176未占用。
新增ownchildbead公开create/read/start/sync后才源码编辑，beforeedit/eachcommit再次actualfetch。
原B/endpoint保存对象与历史cold receipts、E/H/Bbaseline、A支持packet/rootreplay全部只读。
A Bcanonical62a45e47905fdc77a953e4bbab38926c10a1f4abb4f5be7b59edde2c2117a71a；
H模型/5044derivedinventory/raw domains严格沿用A，不重新producer/cold-check。

目标：以A26cliques/41parents为起点，在同100k总pair预算中寻找55unknown的正支持。
从精确重建且fresh验证的Arefs推导每owner已支持parent计数，不相信packet计数。
固定priority按(支持数,owner)升序，B为17,18,19,22,10,8；owner内部row升序。
必须完整96row permutation（exactset+length/type，无重复/省略），包括已支持行随后skip。
其余forward-MRV、candidate排序、binary predicate、core/domain/parent身份均不变。
不能把新覆盖单独归因于调度或称speedup：A起点H7/18，B起点A26/41不同。
不授权同seed numeric比较基线，仅ONE目标；零新增则退休此调度实验，不尝试第三顺序。

允许文件：packing/devtools/probe_n17_raw_row_support.py的optional full row_order参数与
严格验证（default numeric行为保持），对应原rawtests仅必要回归；新
packing/devtools/probe_n17_scheduled_row_support.py与tests/test_n17_scheduled_row_support.py；
session176、X048-session-176-owner-priority/{README.md,receipts/*}, native176一次和必要
map/integrity/SYNOPSIS/ledger/close/resource entries；localcontrol/p02b-*,runs/p02b-*，
handoff/P02B_RETURN.md。A/H/kernel/producer全部不编辑，旧B–J/G/I、A全部冻结。

Fresh26Aseed pair验证计入空globalcache，全部通过前不能记coverage；source/replay packet
identity、full26prefix、exact(rawindex,half)/strictcore/domain/model/provenance绑定。
fullroworder参数拒绝partial/duplicates/unknown/noninteger，不能subset→ALL。
正packet以新schema记录实际完整schedule和输入；replay重建refs，无DFS/cache，直接
每selection15pairs，推导parentcoverage/increment vs41；不信任search或rowclaims。
公开源码身份用Gitrevision/path，不复制localgate Gitfilebytehash；runtimeartifact hash保留。

资源：ONE B100000unique exactpairs含seedcost，100000DFS，180s/512MiB，immutable
control/supervise.py Job240/free8GiB。任何guard结束一次attempt，不扩大或重跑研究目标。
Freshrootreplay120s/512MiB/Job150；endpointcontrol/replayJob45。Input64MiB/packet4MiB，
raw4096/derived8192 ceiling和fixtureexact5044/96保持。A实测100kpairs157.625s170758144B，
B时间/覆盖不确定，180sguard可能先到；不以历史数据宣称cold speedup。

Controls/验收：现有raw default/fixed/MRV回归，完整置换与有限图穷举支持集一致；
partial/重复/非法row order拒绝；seed/provenance/receipt/coverage tamper；allseedcharged、
failedquery不cache；memory/time/pair/node guards；endpoint full angle-containing child与
freshpositive replay。Focusedtests/Ruff/types和root source/control GO之后才ONE B。
独立新parent>=1为有效增量，full26prefix/41baseline必须保留；all96仅此模型whole-parent
删除route结论。Guard/搜索失败/负exhaustion=>unknown/unverified，不是unsupported/admission。

自动白名单：ownedbead/session/Git/Draft333、必要formalstack现有层记录、控件/一次目标/
独立回放、自有CI确定性最小修复+focusedtest+push+终态观察；readonly ownership/parent同步。
禁止307write/merge/mainmerge/rebase/forcepush/kernel/producer/capture/Flag2/admission/newsolver/
全图bruteforce/capladder/CI阈值或测试削弱/lockfile/credential/globalconfig/他人事务/删除证据。
host3.12仅stdlib工具，project3.14显式解释器；每新PS先Enter-Environment，复杂脚本parse。
冲突仅停受影响源码，保留已接受证据；资源或clock结束保留partial，不以失败断言负结果。

终点：有限正增量或honest bounded-no-increment + root独立replay接受 + exactsource及final
metadata fast/required CI终态、自有beadclosed/synced、真实clock/native一次lowerbound/RETURN。
可真实stopped/admin-close/certpending直到sourceancestor实际PASS，再clear并观察finalmeta。
CI队列不延长executorclock；restore依靠保留原revision/artifact，不自动回滚或删文件。
项目后由新W3选择实质机制，禁止机械ordering/cap续跑；cached primitive adapter仅后续候选。
