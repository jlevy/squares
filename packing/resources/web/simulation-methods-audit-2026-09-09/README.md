# Simulation and physics-method source audit, 2026-09-09

This directory is the frozen discovery packet for
[the simulation mechanisms research report](../../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md).
It retains the actual arXiv, Crossref, OpenAlex, Semantic Scholar, GitHub and publisher
responses used to locate that report's sources, so a later agent can inspect the same
corpus without repeating the searches. It is a bounded query receipt, not a claim that
every publication surface was exhausted.

The report's subject is **physics-style and simulation mechanisms** as distinct from
stochastic search over an objective: growth and collision, containers that deform,
constraint projection, non-smooth contact solvers, smoothed penalties with continuation,
and differentiable simulation used as an optimiser. That corpus is the hard-particle
physics, computational-geometry and computer-graphics literature, none of which the
2026-08 square-packing refreshes or
[the 2026-09-08 annealing audit](../annealing-methods-audit-2026-09-08/README.md) were
looking for. That is the gap this pass closes.

The pass ran as four disjoint lanes, and every retained file carries its lane in its
name:

| Lane | Topic |
| --- | --- |
| `laneA-` | Lubachevsky-Stillinger inflation, event-driven molecular dynamics, billiard algorithms |
| `laneB-` | Adaptive shrinking cell, contact dynamics, rigid-body solvers with exact non-penetration |
| `laneC-` | Position-based dynamics, projection methods, differentiable simulation |
| `laneD-` | Smoothed penalties with continuation, nonlinear-programming packing, circle-literature mechanisms |

## What was retained

- **72 papers**, each as the original PDF plus a faithful `pdftotext -layout` extraction,
  the extraction method this archive already uses. None carries a cleaned transcription;
  they are **raw-only** entries under
  [the archive index's](../../README.md) stated convention.
- **One OCR sidecar**, for the single retained source whose PDF is an image-only scan.
- **101 index and source responses** in this directory.

## Search receipts

Every request below was issued from this checkout with `curl` on 2026-09-09. Times are
UTC. The arXiv feeds each retain their own query URL in a `<link rel="self">` element and
their result count in an `<opensearch:totalResults>` element; every OpenAlex response
retains its own request path in `meta.x_query.url`. The `Request` column below is read
from those retained bytes wherever the file carries it.

| Receipt | Retrieved (UTC) | Request | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `laneA-arxiv-query-author-lubachevsky.xml` | 2026-09-09T07:24:41Z | <https://arxiv.org/api/query?search_query=au:%22Lubachevsky%22&start=0&max_results=60&id_list=> | 32026 | `0f6a95e46104aeb798dad45e1ba07a03abfc2e85446023ada984d086f6925646` |
| `laneA-arxiv-query-event-driven-nonspherical.xml` | 2026-09-09T07:24:24Z | <https://arxiv.org/api/query?search_query=abs:%22event-driven%22+AND+(abs:%22packing%22+AND+(abs:%22polygon%22+OR+(abs:%22polyhedra%22+OR+abs:%22nonspherical%22)))&start=0&max_results=60&id_list=> | 6442 | `f6be85c57e7584224ed18b5a6f50e3d06b1caadfca8785abae7d9f2fcdf3b41f` |
| `laneA-arxiv-query-hard-squares-superball-jammed.xml` | 2026-09-09T07:25:13Z | <https://arxiv.org/api/query?search_query=(abs:%22hard+squares%22+OR+(abs:%22hard+rectangles%22+OR+(abs:%22superball%22+OR+abs:%22superdisk%22)))+AND+(abs:%22jammed%22+OR+abs:%22packing%22)&start=0&max_results=60&id_list=> | 93410 | `b4e843c1b980d28653be87786bb808c7cc19a60363fa961023930a247db16abb` |
| `laneA-arxiv-query-lubachevsky-and-stillinger.xml` | 2026-09-09T07:24:20Z | <https://arxiv.org/api/query?search_query=all:%22Lubachevsky%22+AND+all:%22Stillinger%22&start=0&max_results=60&id_list=> | 23755 | `adcf7cedb8b578085b25673c53dd753775688858db5b87cbe5890a30229f7196` |
| `laneA-arxiv-query-lubachevsky-stillinger.xml` | 2026-09-09T07:23:52Z | <https://arxiv.org/api/query?search_query=all:%22Lubachevsky-Stillinger%22&start=0&max_results=60&id_list=> | 18559 | `937bfb0930e7ad78dec2ac9ea8cb14af08c0d42f6c7e3ed5da9c5f900f498e17` |
| `laneA-arxiv-query-skoge-hyperspheres.xml` | 2026-09-09T07:31:19Z | <https://arxiv.org/api/query?search_query=ti:%22Packing+hyperspheres+in+high-dimensional+Euclidean+spaces%22&start=0&max_results=10&id_list=> | 4677 | `dd5edc853ed7015d77da233735a13b8454402d9a22758e8d95929e22ef7c64a7` |
| `laneA-github-dynamo-interactions-listing.json` | 2026-09-09T07:29:00Z | <https://api.github.com/repos/dynamomd/DynamO/contents/src/dynamo/dynamo/interactions> | 28054 | `9d994670674793d729e5aabe145eb81fdf5f9e39b473a1fb92b50f8ceee7e29a` |
| `laneA-github-dynamo-parallelcubes-probe.json` | 2026-09-09T07:28:59Z | <https://api.github.com/search/code?q=ParallelCubes+repo:dynamomd/DynamO> | 120 | `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e` |
| `laneA-github-dynamo-parallelcubes-source.cpp` | 2026-09-09T07:29:14Z | <https://raw.githubusercontent.com/dynamomd/DynamO/master/src/dynamo/dynamo/interactions/parallelcubes.cpp> | 4096 | `6d6511ff5196d300200885a94fed6f07f62d2ae7a929f26e2c8ecb5cb3bc552d` |
| `laneA-github-packing-generation-readme.md` | 2026-09-09T07:29:11Z | <https://raw.githubusercontent.com/VasiliBaranov/packing-generation/master/README.md> | 27116 | `f9b6404488331a1a50b90ef659c594636edf71d24b62a713f9e72c761f7eb8a3` |
| `laneA-openalex-probe-ls1990-random-disk-packings.json` | 2026-09-09T07:27:30Z | <https://api.openalex.org/works?filter=title.search:geometric%20properties%20of%20random%20disk%20packings&select=...> | 1695 | `fa0484395cf3403141eacd0ce02fe2c5bb45e693c76d811ca2ca243f9936bd0c` |
| `laneA-openalex-probe-lsp1991-disks-vs-spheres.json` | 2026-09-09T07:34:08Z | <https://api.openalex.org/works?filter=title.search:disks%20versus%20spheres%20contrasting%20properties%20of%20random%20packings&select=...> | 554 | `05e1b2e5d5b2ae70b10e7e45434b2bd01078d8e9ee7daa83d7751769e8c0b1c7` |
| `laneA-openalex-probe-lsp1991-doi.json` | 2026-09-09T07:34:23Z | <https://api.openalex.org/works?filter=doi:10.1007/BF01048304&select=...> | 1570 | `e1333e3db6cd25c0a448ed5357ebbcd4b8390f34cf56741e3e12bd961261ee8b` |
| `laneB-arxiv-query-adaptive-shrinking-cell.xml` | 2026-09-09T07:24:09Z | <https://export.arxiv.org/api/query?search_query=all:%22adaptive%20shrinking%20cell%22&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending> | 19917 | `3107658ac153cd3e6d8306030105a496a6a6d691c637fca21e0dd62008247656` |
| `laneB-arxiv-query-azema-polygons.xml` | 2026-09-09T07:37:04Z | <https://export.arxiv.org/api/query?search_query=au:Azema_E&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending> | 3479 | `cad97efa9aacfcffa1c55817cc6b7ba081c58d97016b65cc5fdf6e8700cadc0e` |
| `laneB-arxiv-query-confinement-packings.xml` | 2026-09-09T07:39:41Z | <https://export.arxiv.org/api/query?search_query=all:%22cylindrical%20confinement%22%20AND%20all:packings&...> | 7912 | `640e1db87b8f980dafb5c1a483839690795e63c010857f86816bdca3436b8090` |
| `laneB-arxiv-query-contact-dynamics-granular.xml` | 2026-09-09T07:24:36Z | <https://export.arxiv.org/api/query?search_query=all:%22contact%20dynamics%22%20AND%20all:granular&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending> | 103459 | `4f8929c26b429b8a6a85bff658b77114502516a6e6d51c1075c77c9d0071ad46` |
| `laneB-arxiv-query-floppy-box-mc.xml` | 2026-09-09T07:39:20Z | <https://export.arxiv.org/api/query?search_query=all:%22floppy-box%22+OR+all:%22floppy%20box%20Monte%20Carlo%22&start=0&max_results=30&...> | 2881 | `5935d0b32836e1856ab8f64eeeb2d28ef1dd9dc3ac84a3dd48fdd1ae4e178b21` |
| `laneB-arxiv-query-lcp-rigid-body.xml` | 2026-09-09T07:29:25Z | <https://export.arxiv.org/api/query?search_query=all:%22linear%20complementarity%22+AND+all:%22rigid%20body%22&start=0&max_results=40&sortBy=relevance&sortOrder=descending> | 24651 | `5a4380e7b887f83f511bb5b712db17a633da4adf47dba00c5bfde9592cdbd79e` |
| `laneB-arxiv-query-nonsmooth-contact-dynamics-signorini.xml` | 2026-09-09T07:25:12Z | <https://export.arxiv.org/api/query?search_query=all:%22nonsmooth%20contact%20dynamics%22+OR+all:%22non-smooth%20contact%20dynamics%22+OR+all:%22Signorini%22+AND+all:%22Coulomb%22&start=0&max_results=60&...> | 60015 | `ce20c1598952ea3c426861833dcf8bcdbfb072e34e5f35ec0cdcee65f5d8489c` |
| `laneB-arxiv-query-superballs-superdisks.xml` | 2026-09-09T07:24:33Z | <https://export.arxiv.org/api/query?search_query=all:superball+OR+all:superballs+OR+all:superdisk+OR+all:superdisks&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending> | 101650 | `e3c56c71fb5e2366d873b24fe9b1ce1e4bcad99ebad1fac30cb02001432de89d` |
| `laneB-arxiv-query-torquato-packings.xml` | 2026-09-09T07:24:11Z | <https://export.arxiv.org/api/query?search_query=au:Torquato_S+AND+abs:packings&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending> | 56487 | `cb876f0a186dfa8209119ddcdf17b706aefd2342cc81692ee36c14384cfe0a8e` |
| `laneB-box2d-solver-defaults.txt` | 2026-09-09T07:35:57Z to 07:36:44Z | grep extraction from raw.githubusercontent.com Box2D `src/types.c`, `src/manifold.c`, `src/physics_world.c` | 5231 | `a34d6b89b2348c35423c2b1d9f9fcbcf25501ff1854931d4794f8b33a43605de` |
| `laneB-bullet-solver-defaults.txt` | 2026-09-09T07:35:52Z | grep extraction from raw.githubusercontent.com Bullet `btPersistentManifold.cpp`, `btContactSolverInfo.h` | 2498 | `e851cf89d750570cc6da3f5fcd9a5650b7f357c7a3c9eb0bab58289f84d0fc85` |
| `laneB-github-implementations-probe.txt` | 2026-09-09T07:35:08Z | <https://api.github.com/repos/{siconos/siconos,projectchrono/chrono,erincatto/box2d,bulletphysics/bullet3,tkoziara/solfec}> | 1190 | `a58e8a9511da709f2d4d46f79c7057f02488e6b9a176a88a79e0c0f070657480` |
| `laneB-github-solfec-lmgc90-probe.txt` | 2026-09-09T07:35:22Z | https://api.github.com/orgs/parmes/repos?per_page=30` and LMGC90 GitLab page | 898 | `ca33edf00a91cc23ee4194a0fe8d979d89710de6f8fb92950b0484627af44d96` |
| `laneB-hal-query-contact-dynamics-title.json` | 2026-09-09T07:27:08Z | <https://api.archives-ouvertes.fr/search/?q=title_t:%22contact%20dynamics%22&fl=...&rows=60&wt=json> | 32806 | `e0eca7fd606fdaeeca95e50502041b1591cabc2e0c9032be0faf5b5c5a9c878d` |
| `laneB-hal-query-moreau-author.json` | 2026-09-09T07:27:10Z | <https://api.archives-ouvertes.fr/search/?q=authFullName_t:%22Jean%20Jacques%20Moreau%22&fl=...&rows=60&wt=json> | 29190 | `d6b4f10dd012e35ea9f1d1db4017ae3182b11d996552f43d3cf1cd91e7d37d8c` |
| `laneB-lmgc90-gitlab-landing.html` | recorded in the file | https://git-xen.lmgc.univ-montp2.fr/lmgc90/lmgc90_user` (raw landing page; saved first as `lmgc.html`, renamed to the `laneB-` prefix) | 36239 | `7528d988f8f45a5b25c498138c54ee3aa59aa6c93003fd219e8423f14b3229d0` |
| `laneB-lmgc90-gitlab-probe.txt` | recorded in the file | https://git-xen.lmgc.univ-montp2.fr/api/v4/projects/lmgc90%2Flmgc90_user` and README raw | 1209 | `ee0e7c703448a2e635b7cfbe9f2744cb90363acb3e7b32c5b0853fa405187369` |
| `laneB-openalex-adaptive-shrinking-cell.json` | 2026-09-09T07:38:54Z | <https://api.openalex.org/works?search=%22adaptive%20shrinking%20cell%22&per-page=50&select=...&sort=cited_by_count:desc> | 95086 | `c34630bdc77bf4427093a2f81188902a4948fdc9e60b5ab9032584451edbe0d3` |
| `laneB-openalex-cd-as-optimiser-probe.json` | 2026-09-09T07:34:26Z | <https://api.openalex.org/works?search=%22contact%20dynamics%22%20densest%20packing%20optimization%20rigid&per-page=30&...> | 17263 | `e7f9cdf5ed801bf86359e51d6a8c9126c6f232ef877d1ae0d9b8db19b82b3bb6` |
| `laneB-openalex-contact-dynamics-search.json` | 2026-09-09T07:26:38Z | <https://api.openalex.org/works?search=%22contact%20dynamics%22%20granular%20nonsmooth&per-page=50&select=...&sort=cited_by_count:desc> | 331145 | `ce2530f8c268afcd35db6f091530c530cf24b786f412409b16339db29534005b` |
| `laneB-openalex-probe-anitescu-potra-1997.json` | 2026-09-09T07:29:46Z | <https://api.openalex.org/works?search=%22Formulating%20dynamic%20multi-rigid-body%20contact%20problems%20with%20friction%22&select=...> | 13887 | `c3362c8aa1d23db42259192e6e20d3409b1e4ff00436ebdf0b6225bdff567aaf` |
| `laneB-openalex-probe-cd-key-dois.json` | 2026-09-09T07:27:52Z | <https://api.openalex.org/works?filter=doi:10.1016/S0045-7825(98)00383-1> | 17134 | `578c57729a8c0d7c3bd49548327f3ad20073ff849bea726782d72a26163a8a6c` |
| `laneB-openalex-probe-jin-chan-2020-confinement.json` | 2026-09-09T07:39:24Z | <https://api.openalex.org/works?search=%22Shape-Anisotropy-Induced%20Ordered%20Packings%20in%20Cylindrical%20Confinement%22&select=...> | 9403 | `4e6a85971bdd29eed4df28ae33b180d1c0ca84962bdd1def98bfe578f0b9eb82` |
| `laneB-openalex-probe-moreau-1994.json` | 2026-09-09T07:28:18Z | <https://api.openalex.org/works?search=%22Some%20numerical%20methods%20in%20multibody%20dynamics%20application%20to%20granular%20materials%22&select=...> | 35332 | `e16de230d160dd1b67743015cfc3c4ad57834337bde66a2214b03721dfa48f3b` |
| `laneB-openalex-probe-preclik-rude.json` | 2026-09-09T07:37:58Z | <https://api.openalex.org/works?search=%22Ultrascale%20Simulations%20of%20Non-smooth%20Granular%20Dynamics%22&select=...> | 9018 | `dc5f2c66936f05ee4f75e0c30a021484d5fd2612f020eee9c762f9a99803ba14` |
| `laneB-openalex-probe-stewart-trinkle-1996.json` | 2026-09-09T07:29:46Z | <https://api.openalex.org/works?search=%22implicit%20time-stepping%20scheme%20for%20rigid%20body%20dynamics%20with%20inelastic%20collisions%22&select=...> | 17753 | `9423b8d79e4e40369f42e53da37c0dc448caaf20ea3363adb60c815d91858e86` |
| `laneB-semanticscholar-oa-probe-cd.json` | 2026-09-09T07:28:14Z | https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=title,year,openAccessPdf,externalIds,isOpenAccess` for 4 DOIs | 1689 | `dc103e0170a82f7ca33164b6e2ef8cd45fa49bf9842de17e1f1f992b69ba6da9` |
| `laneB-solfec-readme-probe.txt` | 2026-09-09T07:35:33Z | https://raw.githubusercontent.com/parmes/solfec-1.0/master/README.md` + contents API | 2479 | `7d5a2376ee3612048a88a18f670cea79e49947f161ebc30a6da6d59e800bb036` |
| `laneC-arxiv-query-alternating-projections-packing.xml` | 2026-09-09T07:31:10Z | <https://arxiv.org/api/query?search_query=all:%22alternating+projections%22+AND+all:%22packing%22&start=0&max_results=40&id_list=> | 5347 | `0c148f5a7ed79e9dac43de2cdba71b38130efb759139184c26ff95a66d5e86a0` |
| `laneC-arxiv-query-difference-map-packing.xml` | 2026-09-09T07:30:12Z | <https://arxiv.org/api/query?search_query=all:%22difference+map%22+AND+all:%22packing%22&start=0&max_results=60&id_list=> | 758 | `1de0279955246f003a5d0b1812e450e344f3a203bb68a0fe053787a809458a9c` |
| `laneC-arxiv-query-differentiable-packing.xml` | 2026-09-09T07:27:26Z | <https://arxiv.org/api/query?search_query=all:%22differentiable%22+AND+all:%22packing%22&start=0&max_results=60&id_list=> | 145823 | `4ac09d0073ae64a8dce95310355bb16c31d2242b973e50215e2a984aa4158c19` |
| `laneC-arxiv-query-divide-and-concur.xml` | 2026-09-09T07:25:10Z | <https://export.arxiv.org/api/query?search_query=all:%22divide%20and%20concur%22&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending> | 17559 | `ff6727cedefabe49424c177a086bbbb18f6c1719dbc81451910bf21e87b7d12b` |
| `laneC-arxiv-query-douglas-rachford-circle-sphere.xml` | 2026-09-09T07:30:08Z | <https://arxiv.org/api/query?search_query=abs:%22Douglas-Rachford%22+AND+(abs:%22circle%22+OR+(abs:%22sphere%22+OR+abs:%22packing%22))&start=0&max_results=60&id_list=> | 14460 | `c9a336ede019e3346e844aa01d1571a0bdf3d28d5fd5925e9ad7b83a1cfe645f` |
| `laneC-arxiv-query-douglas-rachford-packing.xml` | 2026-09-09T07:29:57Z | <https://arxiv.org/api/query?search_query=all:%22Douglas-Rachford%22+AND+all:%22packing%22&start=0&max_results=60&id_list=> | 762 | `ea3e46869942a3230b78976bffaf16e1bb522de564058ccc260567caf4e3ad37` |
| `laneC-arxiv-query-elser-author.xml` | 2026-09-09T07:25:32Z | <https://export.arxiv.org/api/query?search_query=au:%22Elser_V%22&start=0&max_results=100&...> | 10984 | `949b6cab32abe803c60f659f0b99f179f1a3cb935e646912803c5e7958d56e9d` |
| `laneC-arxiv-query-pbd-packing-phrase.xml` | 2026-09-09T07:31:28Z | <https://arxiv.org/api/query?search_query=all:%22position+based+dynamics%22+AND+all:%22packing%22&start=0&max_results=40&id_list=> | 776 | `271fb454f7211fffa9c7215d44ebbe34980543f2540cd57cbf16131b0c339d45` |
| `laneC-arxiv-query-position-based-dynamics-packing.xml` | 2026-09-09T07:31:07Z | <https://arxiv.org/api/query?search_query=all:%22position-based+dynamics%22+AND+all:%22packing%22&start=0&max_results=40&id_list=> | 776 | `b4565e2c36dd7e7df10d76a236c3d2c125b6572def7e13b989f13bbfb114eb45` |
| `laneC-arxiv-query-position-based-dynamics.xml` | 2026-09-09T07:25:13Z | <https://export.arxiv.org/api/query?search_query=all:%22position%20based%20dynamics%22&start=0&max_results=60&...> | 100582 | `f836163b47f34e8ae751f17e2358b8148f7e0c4ab3b3365a36dff4a93ba8b93a` |
| `laneC-arxiv-query-projection-methods-square-packing.xml` | 2026-09-09T07:31:03Z | <https://arxiv.org/api/query?search_query=all:%22projection%22+AND+all:%22square+packing%22&start=0&max_results=40&id_list=> | 764 | `5d9f8f30ab25772376465b86dd992b8d11dda0b72ebf3fe75617ec89c8d07444` |
| `laneC-arxiv-query-rrr-relaxed-reflect-reflect.xml` | 2026-09-09T07:25:44Z | <https://export.arxiv.org/api/query?search_query=all:%22relaxed-reflect-reflect%22+OR+all:%22relaxed+reflect+reflect%22+OR+all:%22RRR+algorithm%22&...> | 15282 | `bdbf2efee97453a2a2552cffb1f5bde52ccf62c68ee4d0c13598d73bda3250c5` |
| `laneC-arxiv-query-square-packing-optimizer-recent.xml` | 2026-09-09T07:31:35Z | <https://arxiv.org/api/query?search_query=all:%22unit+squares%22+AND+(all:%22packing%22+AND+all:%22optimization%22)&start=0&max_results=40&id_list=> | 24608 | `aaac8b07113dabd421842c82493e5baece3cd07ef7e671bcf381829899a66ab6` |
| `laneC-arxiv-query-xpbd.xml` | 2026-09-09T07:31:31Z | <https://arxiv.org/api/query?search_query=all:%22XPBD%22&start=0&max_results=40&id_list=> | 25964 | `5c872cdbeafb956695eb9d5b1befa4b61870af6ce8a3e781f70dd6446a29a4a7` |
| `laneC-github-repo-probes.json` | recorded in the file | https://api.github.com/repos/{...} x13 | 3067 | `c764f90d1a6af73d8c2c23138e6c0bea8f9437dc086a834a16b5654fde1c6570` |
| `laneC-github-veitelser-repos.json` | 2026-09-09T07:36:11Z | <https://api.github.com/users/veitelser/repos?per_page=100> | 41818 | `ac3334f75a944019cb7cd6e84226e6fad82ec2f12ac862dfc7bf33627c917056` |
| `laneC-openalex-cites-kallus-2010.json` | recorded in the file | <https://api.openalex.org/works?filter=referenced_works:W2083379047&per_page=50> | 4671 | `c5c75e8f844e7db60b3c1353f5f1b89b1d22b56ca3d20dcfa3493e2c6628b47a` |
| `laneC-openalex-elser-book-projections.json` | 2026-09-09T07:37:59Z | <https://api.openalex.org/works?filter=doi:10.1017/9781009475518&...> | 3402 | `dfc03f1fae23773f05ff1ec0168934c4122a73c017a44c638ef5bfcccf8dbb19` |
| `laneC-openalex-elser-packing.json` | 2026-09-09T07:33:35Z | <https://api.openalex.org/works?filter=default.search:%22divide%20and%20concur%22%20packing&...> | 8913 | `ea29e37e9cce09b53a90d9c38cb648eca42925dffad2f4606f423603a74d9ad1` |
| `laneC-openalex-geometric-puzzles-divide-concur.json` | 2026-09-09T07:33:50Z | <https://api.openalex.org/works?filter=default.search:%22Solving%20geometric%20puzzles%20with%20divide%20and%20concur%22&...> | 4046 | `1d4e549a6540866e9fd0b7ab33d2c04bfc4695a548a5ebf239ce1e4faed8d576` |
| `laneC-openalex-gravel-elser-2008.json` | 2026-09-09T07:30:58Z | <https://api.openalex.org/works?filter=doi:10.1103/physreve.78.036706&select=...> | 2313 | `a387a2689906a9b734edf5687504d81dea963dabe875641c196cefa587d3bb88` |
| `laneC-openalex-kallus-2010-id.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1103%2Fphysreve.82.056707> | 474 | `6304cd2c425d348b0e651c488e763df6eae2eeb9f31eae439c8395ab6b166d9b` |
| `laneC-openalex-pbd-packing-optimization.json` | 2026-09-09T07:37:23Z | <https://api.openalex.org/works?filter=default.search:%22position%20based%20dynamics%22%20packing%20optimization&...> | 10269 | `b03c5ea406bfa2d8083cbc0ba1b4b3da126c002e0a2ef733c0ca118b6a73e572` |
| `laneC-openalex-physics-simulation-irregular-packing.json` | 2026-09-09T07:37:24Z | https://api.openalex.org/works?filter=fulltext.search:physics simulation irregular object packing container&per_page=25 | 10558 | `35a31db02a17a91dfc13a4be02647f04c1d89952c4427a2579554e537e3f21da` |
| `laneC-openalex-zhuang-2024-dynamics-packing.json` | 2026-09-09T07:37:45Z | <https://api.openalex.org/works?filter=default.search:%22Dynamics%20simulation-based%20packing%20of%20irregular%203D%20objects%22&...> | 16282 | `d7423ece2b685e43ed24ce9c05bcc56f67c54ec04ebeecb6e0f820dd239a5f40` |
| `laneD-arxiv-query-circle-packing-continuation.xml` | 2026-09-09T07:25:26Z | <https://arxiv.org/api/query?search_query=all:%22circle+packing%22+AND+all:%22continuation%22&start=0&max_results=60&id_list=> | 33574 | `f3f6b7fa28e25368d2d9d4313102a3ecb5ea47020e79fc57c138e45bcd4798c1` |
| `laneD-arxiv-query-distance-geometry-smoothing.xml` | 2026-09-09T07:25:51Z | <https://arxiv.org/api/query?search_query=all:%22distance+geometry%22+AND+all:%22smoothing%22&start=0&max_results=60&id_list=> | 5963 | `ded1b65cb4dc2d1b5333e99964647f76e6b61ac051ca76133d6e366fa96fef90` |
| `laneD-arxiv-query-energy-landscape-paving.xml` | 2026-09-09T07:26:38Z | <https://arxiv.org/api/query?search_query=all:%22energy+landscape+paving%22&start=0&max_results=60&id_list=> | 5047 | `8a2e4a5a628e53a3c29cfef95e34837dedf16a4141a208c9cd5b93d372170280` |
| `laneD-arxiv-query-equal-circles-in-a-square.xml` | 2026-09-09T07:26:45Z | <https://arxiv.org/api/query?search_query=all:%22equal+circles%22+AND+all:%22square%22&start=0&max_results=60&id_list=> | 2793 | `8703f316b4bc4477f5deb99dbeaa36dab2582f9cde35dfa11eb221dffca7f8e7` |
| `laneD-arxiv-query-formulation-space-search.xml` | 2026-09-09T07:26:42Z | <https://arxiv.org/api/query?search_query=all:%22formulation+space+search%22+OR+all:%22reformulation+descent%22&start=0&max_results=60&id_list=> | 6130 | `9dad22910c3fc50dd24c278c10b6fc9f2318c826dcca2fa06a7ee399f6a1a93f` |
| `laneD-arxiv-query-graduated-nonconvexity.xml` | 2026-09-09T07:25:47Z | <https://arxiv.org/api/query?search_query=all:%22graduated+non-convexity%22+OR+all:%22graduated+nonconvexity%22&start=0&max_results=60&id_list=> | 92335 | `4ee8121020e37aeb53519276443970652b4cd810131fda33ede0e58b40a30bef` |
| `laneD-arxiv-query-packing-augmented-lagrangian.xml` | 2026-09-09T07:25:55Z | <https://arxiv.org/api/query?search_query=all:%22packing%22+AND+all:%22augmented+Lagrangian%22&start=0&max_results=60&id_list=> | 7691 | `451e4e91b92591301568f2182d9f2ea06cdf770fce67d9ac58a207f7dd7d1df7` |
| `laneD-arxiv-query-phi-function-packing.xml` | 2026-09-09T07:25:58Z | <https://arxiv.org/api/query?search_query=all:%22phi-function%22+OR+(all:%22phi+function%22+AND+all:%22packing%22)&start=0&max_results=60&id_list=> | 76630 | `95e26678abfac06a10ebf5cd5c0fefe396a37a2ccdb22d013927202ab5c10b64` |
| `laneD-arxiv-query-quasi-physical-packing.xml` | 2026-09-09T07:26:35Z | <https://arxiv.org/api/query?search_query=all:%22quasi-physical%22&start=0&max_results=60&id_list=> | 50703 | `2cc23378de7e57dfc5f05ecceebb56e2671f4425e271b7a241b6761f81571e0e` |
| `laneD-openalex-elp-circle-packing.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:energy landscape paving circle packing&per_page=20 | 152724 | `b9d49d4f414e2cb760133d25f322d728785a131f83dca74667ae13ac2c6cb500` |
| `laneD-openalex-elp-packing2.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:energy landscape paving packing equal circles container&per_page=20 | 112395 | `b728111efba023080b4b5473ea3099df37caf33b454c208bf20ad19ab79bd6f7` |
| `laneD-openalex-formulation-space-search.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:formulation space search circle packing&per_page=25 | 122905 | `84cd0fb8fe7cb01f57f9877d20722a72d510219e51caf62e8c6518c8d2925807` |
| `laneD-openalex-phi-function-technique.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:phi-function technique packing irregular objects&per_page=20 | 160923 | `cb3af9fc4c833d65c25e6393710a2573a36f43d5fb74057f3b0bf0e20d890c41` |
| `laneD-openalex-polygons-continuous-rotation.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:packing convex polygons continuous rotations phi-function nonlinear&per_page=20 | 113572 | `ff36fc51959c58e450e1f335d0c07968c843a68107338273144401664fea8448` |
| `laneD-openalex-probe-10-1007-978-3-540-74446-7_20.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1007%2F978-3-540-74446-7_20> | 1629 | `7c309ad419f49ec51abf0f58878718d98c3e5e1c5c6d218100bbf70dfbfaf1d9` |
| `laneD-openalex-probe-10-1007-PL00009306.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1007%2FPL00009306> | 2605 | `89d12acb5da0ba81ee1e00088c44bbd4db3af913218cea7e62a0b756cd898354` |
| `laneD-openalex-probe-10-1007-PL00009472.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1007%2FPL00009472> | 2613 | `70a42041ba0df0a4a2df841fe6895ac09d888bb17a083b6b582351336220410a` |
| `laneD-openalex-probe-10-1016-j-cie-2009-05-010.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1016%2Fj.cie.2009.05.010> | 1581 | `9748cea5a1b08a51a90e352f1b3c76bb99d792065d9e903ca6797ebf54d28e8a` |
| `laneD-openalex-probe-10-1016-j-comgeo-2009-12-003.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1016%2Fj.comgeo.2009.12.003> | 2503 | `72bdc94cd3d12f1dd65d347c85b6a27239c218109bb3310ecbc821c830624de5` |
| `laneD-openalex-probe-10-1016-j-cor-2004-03-010.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1016%2Fj.cor.2004.03.010> | 1519 | `a4953891249d21c2e710a09e15dae03696063422dd8697bf355bd2e63f461514` |
| `laneD-openalex-probe-10-1016-j-cor-2017-12-002.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1016%2Fj.cor.2017.12.002> | 1562 | `800a031916aaaaaada239d171af4dcc04b7ee05a0401092c2bd94f9aa20c360b` |
| `laneD-openalex-probe-10-1016-j-ejor-2018-01-025.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1016%2Fj.ejor.2018.01.025> | 2473 | `ae398f6eecc8f6eccd4b3c09c40d4b53a1b3746d52219ed762b87d3caff4b64b` |
| `laneD-openalex-probe-10-1016-j-physa-2015-02-092.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1016%2Fj.physa.2015.02.092> | 1629 | `20477a8dc4d7b4cb8e45080d3b4f76c740513f77d4a551e74665328eddd48873` |
| `laneD-openalex-probe-10-1109-cinc-2009-195.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1109%2Fcinc.2009.195> | 1121 | `c02eca6a69491dc3566b45c78bbff9ef0306c303df0e16dedf29a1910dfae10f` |
| `laneD-openalex-probe-10-1137-S1052623495283024.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1137%2FS1052623495283024> | 1573 | `6f398ce246a3ca53e9d05b3408f46e1af8e1b7083f8bdd52b226935f13c9951a` |
| `laneD-openalex-probe-10-1155-2009-150624.json` | recorded in the file | <https://api.openalex.org/works?filter=doi:10.1155%2F2009%2F150624> | 2678 | `41f289fc9084503c2b11f8c94680a410e355dbd5f0b58db94533e073b44dfa0b` |
| `laneD-openalex-probe-stoyan-yaskov-2004-strip.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:mathematical model solution method placing various-sized circles into a strip&per_page=5 | 34088 | `601f41e9a5c8b929e6fe06c376c4e6d8be900012003bd1b13d74f6b2bc3d67df` |
| `laneD-openalex-quasi-physical.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:quasi-physical quasi-human circle packing&per_page=25 | 144028 | `97f44c4b2b3453306a8cc5d60ff14f9106e7d2cc1133759e867cfe4aef925db7` |
| `laneD-openalex-reformulation-descent.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:reformulation descent circle packing&per_page=25 | 206037 | `a3164666a43c8b5ec3730c09997dd6a52b9cd8cb965dd2ea15d18a5cc60c6761` |
| `laneD-openalex-stoyan-yaskov.json` | recorded in the file | https://api.openalex.org/works?filter=fulltext.search:Stoyan Yaskov phi-function packing circles&per_page=20 | 116544 | `afa681a254432f317b002f91d84c0cb1bb672f5c5c5f4320e14b69e156a146af` |
| `laneD-packomania-circles-in-a-square.html` | 2026-09-09T07:46:5xZ | <https://www.packomania.com/csq/csq.html> | 1091866 | `a9ba8e55f9b7533bb65d5308c9ac4f38c731beb092ceff4fbb6631fd8217a20d` |
| `laneD-packomania-index.html` | 2026-09-09T07:46:5xZ | <https://www.packomania.com/> | 19461 | `0c496b2e08636ce8603c7d5ff7abda2817dd34fa5cbfb7f3f4f7f5658af91776` |
| `laneD-semanticscholar-10-1007-PL00009306.json` | 2026-09-09T07:28:49Z to 07:28:53Z | <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/PL00009306?fields=title,year,externalIds,openAccessPdf,isOpenAccess> | 398 | `5144b7f7f6afccf99aff669cc62108c16119401cfd783ace33259f653228f105` |
| `laneD-semanticscholar-10-1007-PL00009472.json` | 2026-09-09T07:28:49Z to 07:28:53Z | <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/PL00009472?fields=title,year,externalIds,openAccessPdf,isOpenAccess> | 404 | `4c90d3a2d5b36a59ff0d4f2c57d2b86562835d8c02cdcd06bad4b02fbce8749f` |
| `laneD-semanticscholar-10-1137-S1052623495283024.json` | 2026-09-09T07:28:49Z to 07:28:53Z | <https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/S1052623495283024?fields=title,year,externalIds,openAccessPdf,isOpenAccess> | 435 | `4aeb4ccd1e38e74501850c621ac011b6fd66a49343c6f5021d747d78ad6e2632` |

## Acquisition manifest

Paths are repository relative and every entry lives under `packing/resources/papers/`,
as `<stem>.pdf` beside `<stem>.raw.md`.

| Source | Acquisition URL | Retrieved (UTC) | PDF SHA-256 | Raw SHA-256 |
| --- | --- | --- | --- | --- |
| `antonova-yang-jatavallabhula-2022-rethinking-optimization-differentiable-simulation` | <https://arxiv.org/pdf/2207.00167> | 2026-09-09T07:32:24Z | `3a7d56e45da4132ea04a7ce4c04f6a8cefc96f5228f56d6b23c573b0c6d9a44d` | `d4d3f5e0a91aa127c099b6c2f2842010492d776208412501b563b68bedf17c8b` |
| `atkinson-jiao-torquato-2012-maximally-dense-packings-2d-noncircular` | <https://arxiv.org/pdf/1405.0245v1> | 2026-09-09T07:25:54Z | `3c51ae3ec591314b7df5a3788b0a263a51f97ff85458d5c4c6ac4eb2c937754f` | `c9e927d7550c38245853be3dda7865aae4209a15201e2a59e4a3dcbbbca6d399` |
| `azema-estrada-radjai-2012-particle-shape-dependence-2d-granular` | <https://arxiv.org/pdf/1208.0499v1> | 2026-09-09T07:37:53Z | `47de3d49d41fe3aea13fd97edb490cbbaaf3ec5704e038d50973b9aa91e46653` | `e99eed7f792d583e927cd6a9c8fa5a01107f131ccc916422320002c7e06fd0d2` |
| `azema-radjai-saussine-2009-quasistatic-rheology-irregular-polyhedral-particles` | <https://arxiv.org/pdf/0805.0178v1> | 2026-09-09T07:37:54Z | `c652f2566e455b7517625d82f5657bcd82fbf4e364ab100cddd61b56226d7e5d` | `f061ec1327be393768d37e65300f10458ff0122cf638ba8be29452c4227314f3` |
| `bannerman-sargant-lue-2011-dynamo-free-event-driven-md-simulator` | <https://arxiv.org/pdf/1004.3501v2> | 2026-09-09T07:28:07Z | `2b58527fc3e8fde5307bbf1a1116b4dea0724033de4115713f91fb2f7da9721e` | `f4238b575d219ad5d15dbd61db433d2c5a0e08709e90d14fdfff39e60a6a7b2b` |
| `bender-muller-macklin-2017-survey-position-based-dynamics` | <https://www.animation.rwth-aachen.de/media/papers/2017-EG-CourseNotes.pdf> | 2026-09-09T07:28:34Z | `386cbba120382662af433cd4df363d01e3a7ec99a1e03d84074fd4e7f703709b` | `08c0d8346e5fbd33fb5b00217602280879055aebad2271a4162d05b3cfd1aba1` |
| `birgin-2016-applications-nonlinear-programming-packing` | <https://www.ime.usp.br/~egbirgin/publications/egbirgin-fmfi2014-contribution.pdf> | 2026-09-09T07:27:45Z | `1c301caf0e73f220f5157a3b75c2a8a1f58601a123cb07adab13f50e0f48f690` | `dbfe81397d261c788fbcb5541cf0b7ddb38c7a287be02c2b55063223b7937ccf` |
| `birgin-gentil-2010-packing-unitary-radius-circles-triangles-rectangles-strips` | <https://www.ime.usp.br/~egbirgin/publications/bg.pdf> | 2026-09-09T07:27:44Z | `13ce329b3d4d2263b98a27e33a9fe67b3f078471ea44a6192605481b74e12fc1` | `8f959777651912e8b98d84d659b45e4f5c4dc790dba7fa3f785f9403f5138b57` |
| `birgin-martinez-nishihara-2006-orthogonal-packing-arbitrary-convex-regions` | <https://www.ime.usp.br/~egbirgin/publications/bmnr.pdf> | 2026-09-09T07:27:47Z | `26283224ca3e861668039047f8b8b7d382b206e08d03f1f0d5b3bc647cf5294c` | `d9e63e4b46460227ebaf37b0350e31833848d4e6e084a3d644ffc31cbdfd6d77` |
| `birgin-sobral-2008-minimizing-object-dimensions-circle-sphere-packing` | <https://www.ime.usp.br/~egbirgin/publications/bs.pdf> | 2026-09-09T07:27:42Z | `1ad477f8ff11dae0bc7de62b07c82e03b98e6319f2ebe6a199f9562b558ead1c` | `03241351c55770d5a7a19c9d8acb24311e3348a410484eacbd35745700c8bf2e` |
| `boll-donovan-graham-lubachevsky-2000-improving-dense-packings-disks-square` | <https://arxiv.org/pdf/math/0405310v1> | 2026-09-09T07:25:09Z | `ca66f1e10cd94c37d0d53909fd849165ebf0d2f6292a7e2b8248facfc31e3027` | `0062d957f7389adde5c22d3fbdcd08118e25f04c71e27b8c5b82692d064e4beb` |
| `debnath-tiwari-sadekar-2025-rasp-shadow-guided-packing` | <https://arxiv.org/pdf/2504.02465v1> | 2026-09-09T07:27:47Z | `aab89aca5f574cdf3eca958a1a5a2e61e87821ce9520202d7abcae2cb1d526f9` | `a937b9aaca57d461e64baca71a4d79323b1bec79165ea13274f77b34bce51723` |
| `donev-torquato-stillinger-2005-neighbor-list-collision-driven-nonspherical` | <https://arxiv.org/pdf/physics/0405089v1> | 2026-09-09T07:25:08Z | `7961f82ac820e7074fff732ce429fa9be83d87624e252214de9fba03bf0e1091` | `92b5a483e76e9d5dba7c7a546b75f4196b1623d5b9bbd8402f502ad6bab0bb16` |
| `dubois-acary-jean-2018-contact-dynamics-method-nonsmooth-story` | <https://comptes-rendus.academie-sciences.fr/mecanique/item/10.1016/j.crme.2017.12.009.pdf> | 2026-09-09T07:29:02Z | `59de61faca8c5a081300b02b39d217369928b03c7910803afa63e52636ada30a` | `1160a6a81fd9f420e6173a878b093c3bb456c16a85bd3d6c1874069affa9b3ac` |
| `elser-2016-complexity-of-bit-retrieval` | <https://arxiv.org/pdf/1601.03428v1> | 2026-09-09T07:29:52Z | `3cc04ad5e29e078fa5d094d3ca883b1a2ec7559148e09397f8f5e8aa5ad93ca3` | `03505fa1eaa31b697a7b25f3a52b60d6aff774aa1d168d5f5d2cc2b5d5a3a6cb` |
| `elser-2019-learning-without-loss` | <https://arxiv.org/pdf/1911.00493v1> | 2026-09-09T07:27:57Z | `69d86f155f384414068303427499152d8cc1c820227c1ac20d3d0aeac00d5fc1` | `9c1e60e0b5e3a64ce5bc7ad110ff1bd88df3f412921391225c3ccf9cef7e9da7` |
| `elser-2023-how-densely-can-spheres-be-packed-moderate-effort` | <https://arxiv.org/pdf/2305.13492> | 2026-09-09T07:33:56Z | `c16b50f0cacab99d1bfccb3a721062de5ed795207d09b0fba0630f773f9031f0` | `61cef5ac82359e20bbb1dc5d5db39149c22b9bb66e63cc4e29e7fd289cb51a19` |
| `fayen-jagannathan-foffi-2020-infinite-pressure-phase-diagram-binary-hard-disks` | <https://arxiv.org/pdf/2003.08889v2> | 2026-09-09T07:39:35Z | `2216f0c706e50af8ee80265b161ebca9cf7d70c2c69859b0bf1ee99840bf16a0` | `72389832e389ba6d2a7bf66d89e839dc3d9421deae8564297d57c7da92227f73` |
| `freeman-frey-raichuk-2021-brax` | <https://arxiv.org/pdf/2106.13281> | 2026-09-09T07:27:22Z | `e3e69a2d75eba75de04b33e12b218c9e52056d073981ebae63b22e6c5e9db212` | `594a530b7fe652e0667e44e431485bf9c2c851bff4c9517178d8964a82715f3e` |
| `fu-steinhardt-zhao-socolar-charbonneau-2016-hard-sphere-packings-within-cylinders` | <https://arxiv.org/pdf/1511.08472v1> | 2026-09-09T07:31:10Z | `9e69598e3870be5183e13da20d136b0162786e32f44eab05f026d992c16e3b63` | `41cc3e767f8f9939c73175aea1ca9eff94ce020918e3ab6cdeafb00f9e12bbf7` |
| `graham-lubachevsky-1995-dense-packings-disks-equilateral-triangle` | <https://arxiv.org/pdf/math/0406252v1> | 2026-09-09T07:27:51Z | `c0accc160378b1dc12174edc6d236c3ccea564d87112e90957702daa02b18f5f` | `1c2049d91c894a2aafd6e704a430b2cead99524d496780a6e19aa2331e907f08` |
| `graham-lubachevsky-1996-repeated-patterns-dense-packings-disks-square` | <https://arxiv.org/pdf/math/0406394v1> | 2026-09-09T07:27:49Z | `e0d43fc5dfc5c8a87eb22b5a86bf54cb6085266abb2f674a16aefddecdf93f65` | `cea60416e754d7d9282dc664e3b934302ce9e1804895fa9ab830cda90716a5e0` |
| `gravel-elser-2008-divide-and-concur` | <https://arxiv.org/pdf/0801.0222v1> | 2026-09-09T07:25:29Z | `6f5602e6c98cf936ab8915477979975a68e7c56cb10953625a86e49fbfc30ce3` | `64e69e848a8277e8cef26db720f435575c488f9d1a562ee4749162c3eac91184` |
| `gupta-raman-2026-differentiable-packing-irregular-3d-objects` | <https://arxiv.org/pdf/2606.16333v2> | 2026-09-09T07:27:40Z | `10b2deb98fd41b6689dbedd32421279e3ff91f446da35344ef3aab87d085ef43` | `82b9923e758deed2e560c4dce788ece1b8bdf2481a1220e8ae2d77db7ab7a840` |
| `hansmann-wille-2002-global-optimization-energy-landscape-paving` | <https://arxiv.org/pdf/physics/0201054v1> | 2026-09-09T07:33:55Z | `0e0404ecc1921c1fecb303d3db0dd212a464bb5b84d7f51f0fddf83338626107` | `6656eadf948366f80c79d39681bc033654bdeb73d80299ef0625e5c438ac05f6` |
| `he-ye-wang-2018-quasi-physical-quasi-human-equal-circles` | <https://arxiv.org/pdf/1611.02323v2> | 2026-09-09T07:33:51Z | `f22c48441d3c1eda1c09d2d24fe4533a1b120782cc23d93521d9f7e204083e9b` | `8ce5d844545fbfb4ba5638e0415735abf69383083525cc431414d0a1c70398b2` |
| `hoover-hoover-bannerman-2009-single-speed-md-hard-parallel-squares-cubes` | <https://arxiv.org/pdf/0905.0293v3> | 2026-09-09T07:25:37Z | `b49cbf803370428a1c3bd3ade2d6127db37936dbacb84b09e8c23c2e6d43b364` | `5aba59ba4b3482955a0eed0bd819daa749b77fe44cdc9a61b434199e001ccb5a` |
| `howell-le-cleach-kolter-2022-dojo-differentiable-physics-engine` | <https://arxiv.org/pdf/2203.00806> | 2026-09-09T07:27:56Z | `729928039c101eba82d02ddfe215d7d19e592414bff32f690014be9f3e071bf7` | `b418f0756bb428c62973a5d221270b3451b1fbd58f39d6d49b3a3fe5d526e0f2` |
| `hoy-2024-ultradense-jammed-ellipse-packings-biased-swap` | <https://arxiv.org/pdf/2409.19196v1> | 2026-09-09T07:32:10Z | `2c81b74a82188359e7f2c805fea7d7249d48d231e6fccbae516c682b0fd2f92a` | `668029ef26578281f5802e162fd55d5399b110d18bfa0b92e2698d5923144823` |
| `hu-anderson-li-2020-difftaichi` | <https://arxiv.org/pdf/1910.00935v3> | 2026-09-09T07:27:05Z | `88837aafd34badf97251153106530ce546705e64630fa7f1d94849b391a6e4be` | `45103a7e0894a26bac0a527d0b270a537c89463cd9c996fe0eb121bd92551420` |
| `jiao-stillinger-torquato-2008-dense-packings-superdisks` | <https://arxiv.org/pdf/0712.0420v1> | 2026-09-09T07:25:38Z | `448b3a44df24baa9672bc827eac50d41417ea5c7925cb439ac25a076a6a05a9c` | `e90c16f66ee7216e423be416cdf228cd332968df218ae010aceb21c7b7719009` |
| `jiao-stillinger-torquato-2009-optimal-packings-superballs` | <https://arxiv.org/pdf/0902.1504v1> | 2026-09-09T07:25:53Z | `6551ddb0ca73f87f31350af92d96fe06f50415be684709169fe6a0a192d3a68d` | `e52072089f55d4c396f1e743adbe08deccdf9c186147f58da0b2b34b8dfbf43b` |
| `jiao-stillinger-torquato-2010-mrj-packings-superballs` | <https://arxiv.org/pdf/1001.0423v1> | 2026-09-09T07:25:36Z | `1f2bb35205827862732018ee3c9fdd337cc45bd63bc102bb041345393afb09f7` | `e08fe4f962af14d3636e9ee7bdd725f2957d63c812ac0585ad3123d885892e59` |
| `kallus-2011-solving-geometric-puzzles-with-divide-and-concur` | <https://ecommons.cornell.edu/bitstreams/0e7b9e1f-a0b3-4dbd-8c49-587e323c0394/download> | 2026-09-09T07:34:08Z | `2d01522cf1958f1827548cf66cfc57a2ba3e90ab33f28b53b72c580aa11dca54` | `1a36f7e2f210f71821517ead3f0ad0f6a72e1b1157da7118e31915d2a2374b72` |
| `kallus-elser-gravel-2010-dense-periodic-packings-tetrahedra` | <https://arxiv.org/pdf/0910.5226> | 2026-09-09T07:33:57Z | `cb28ced59ea8f513bcd88b63808e602591de1ce7da7ae4ffb3e547a41b0749b6` | `e74f8de3acb0c18d4a639c28962b6e610768101f390c376b72713f38fe48616e` |
| `kallus-elser-gravel-2010-method-dense-packing-discovery` | <https://arxiv.org/pdf/1003.3301v2> | 2026-09-09T07:25:29Z | `c21ffc4b18260696a650c6cc7d27fab090c27e9ca94b45eda2d8db7646b65ad1` | `9af5ed6cf3d2bc02efa3407f46425237a3cdcacd17028d1b469398669d58221b` |
| `klement-engel-2021-newtonian-event-chain-monte-carlo-collision-prediction-polyhedra` | <https://arxiv.org/pdf/2104.06829v1> | 2026-09-09T07:29:56Z | `facfe324edee7e15d8a06e7c6826c1701edba20a67f04a12cde1c16f46028c08` | `f910c0d7b0168028ac173e5355384c8835eb8e1d22e243f4ec187b5f2b1043dc` |
| `lal-2025-flow-limit-reflect-reflect-relax` | <https://arxiv.org/pdf/2512.23843v1> | 2026-09-09T07:29:51Z | `e24134c9f2dc44c20b3dea429f46a971ff0fa6bc54d5ba080b998a5c855dc0e1` | `a3b18e0ec786b31481d9d6c2cec3082dde3809944bebf9749b1d8b9e1f67ecb1` |
| `lopez-beasley-2018-packing-unequal-rectangles-squares-formulation-space-search` | <https://arxiv.org/pdf/1802.07519v1> | 2026-09-09T07:33:58Z | `91996ec6dbec2e02710c77c3644c4038d18ce1d1ead759297ce6b219da61689f` | `550f1e80034482efbc014efffa7a39947fc3870fc8a02ef6c85e541b7906adb4` |
| `lubachevsky-1991-how-to-simulate-billiards` | <https://arxiv.org/pdf/cond-mat/0503627v2> | 2026-09-09T07:25:07Z | `ca5633c26c462460bdf341136ffdac282dfae7069afdf068cb13070971340da6` | `98e92e766a0b3f865a76fec54167f3c9a4191289e9a9a0d155f1ae5da0d4c57d` |
| `lubachevsky-graham-1997-curved-hexagonal-packings-disks-circle` | <https://arxiv.org/pdf/math/0406098v1> | 2026-09-09T07:27:52Z | `ac4f1b8208b9ffda2e9c3a9fd52e2c19824fa01990bffc0886e83213b1fe86c4` | `1fb9bf67719f1ab34a56dfb0416784cc943b0fb48a49a8011839179d480064a7` |
| `macklin-muller-chentanez-2016-xpbd` | <https://mmacklin.com/xpbd.pdf> | 2026-09-09T07:26:53Z | `2e8a2030db7999bd425e469bbb798387b74151e3e10c1625d269a7cd75fb0395` | `767ffb011dc5f2ef828bcc7b3fb5691cb369b18a110d92444fb3ad1dbeb217b6` |
| `macklin-storey-lu-2019-small-steps-physics-simulation` | <https://mmacklin.com/smallsteps.pdf> | 2026-09-09T07:26:54Z | `658cb1428a7c34af6419a59fcb1652f25dd8f6cca9472687b337ed9f2f0efca8` | `8d5d4aa74d17e220517c80705d279539059d9289e74f677e7294276fecf20916` |
| `maher-stillinger-torquato-2021-kinetic-frustration-2d-convex-packings` | <https://arxiv.org/pdf/2103.06290v1> | 2026-09-09T07:25:56Z | `17eb5bf411db4565b5a3c50caf625ce2e752b90263c254d2506e861bf285b084` | `5e0dba8ab1dc883654d27445f80aa052e498df1785bdad59eac49b1ed61277e4` |
| `mazhar-heyn-pazouki-2013-chrono-parallel-multiphysics-library` | <https://ms.copernicus.org/articles/4/49/2013/ms-4-49-2013.pdf> | 2026-09-09T07:29:04Z | `d6769a68ab009b1b1c9319bdf2e65429abe68990c7411747da355b1fb1de6e41` | `53e68b02cffa9e375107d26c9ed2721a28bf2e1fb06cc6e4bb7a359bc80af3cb` |
| `metz-freeman-schoenholz-2021-gradients-are-not-all-you-need` | <https://arxiv.org/pdf/2111.05803> | 2026-09-09T07:27:22Z | `3a9ac3c369d5e5aa963ee9584edd40b079b0e7cad333a5e834840ca1191c4bbf` | `222abc65bffeeab0d8cf9619d3e7a17f6631eb246ec4ab5d6dd7688945282cea` |
| `more-wu-1997-global-continuation-distance-geometry` | <https://www.osti.gov/servlets/purl/510547> | 2026-09-09T07:30:01Z | `0b781e0b2efc4fe6b50a7fa677e20e8a09059a433a4947eae107931ed3399909` | `98c3689f37aa605365100f6c2597bfd2e83f4bd296667130b844228fd68bcfba` |
| `muller-heidelberger-hennix-2007-position-based-dynamics` | <https://matthias-research.github.io/pages/publications/posBasedDyn.pdf> | 2026-09-09T07:26:52Z | `8823d1b0549e84c56e0c3cbbf5db3cd00dbd59858835f4d012b64604aac2f4b0` | `c742d4bfe48381e10f85cbc3cfeb23e463db59bd1938e0577c04b2eab6fe7cb8` |
| `muller-macklin-chentanez-2020-detailed-rigid-body-xpbd` | <https://matthias-research.github.io/pages/publications/PBDBodies.pdf> | 2026-09-09T07:26:57Z | `58e4ceb2e12f387adbea906c541f5e63c96e454ccefe865dc29eeebf71db8a47` | `85886faa842e734f444ef3ab44caaa53ddbb33d53258592f08da22fde3eb51ed` |
| `nurmela-ostergard-1997-packing-up-to-50-equal-circles-in-a-square` | <https://web.archive.org/web/2020id_/https://link.springer.com/content/pdf/10.1007/PL00009306.pdf> |  | `52d7681c56a9146863d6f6a0342ed57147feb0e524216fd55a418562920b2db8` | `81f0af3a0dbaf8dfd5c10cab75e252734577c64a519fa6eff709406bd6d5d4a0` |
| `nurmela-ostergard-1999-more-optimal-packings-of-equal-circles-in-a-square` | <https://web.archive.org/web/2020id_/https://link.springer.com/content/pdf/10.1007/PL00009472.pdf> |  | `eb598bc0f11116c940d3835c6200711f54f38ae477d70f4ac7d582496e58b3ad` | `eea991d163b508edf17c92c1cab5253317fb42b2eb0debc9684d10dffbac5cbb` |
| `olsen-kamrin-2018-force-indeterminacy-contact-dynamics` | <https://arxiv.org/pdf/1805.07437v1> | 2026-09-09T07:26:33Z | `d5ddcda1cd663ef7abd6b78c9148b7a71a3aa108c3a41082bbe0f1ad2436e491` | `a85f3def89bfee8074543bd79afd3ceb03a8d2b9e705e906a4666b6b9607a8d5` |
| `peralta-andretta-oliveira-2018-irregular-strip-packing-free-rotations-separation-lines` | <http://www.scielo.br/pdf/pope/v38n2/1678-5142-pope-38-02-195.pdf> | 2026-09-09T07:42:47Z | `d2f1a359b1f847829ff4ec2215fe09d0239241ca72a5c8a5417f46d059f37907` | `825608138903f319256c7d0e1c0f5697809928f219521baa72acef1bbc1bfcfe` |
| `preclik-rude-2015-ultrascale-simulations-nonsmooth-granular-dynamics` | <https://arxiv.org/pdf/1501.05810v1> | 2026-09-09T07:38:05Z | `aa1d038519f03af467285d62ab8dee819f3d842330727b0457c85dde98692051` | `b8b1edb890bf37091c9aaab755441d673d38c1415d2f4f78c279fee90f5a3a3a` |
| `romanova-bennell-stoyan-2018-packing-concave-polyhedra-continuous-rotations` | <https://web.archive.org/web/2020id_/https://eprints.soton.ac.uk/418130/1/EJOR_Concave_polyhedra_002_.pdf> |  | `0a0152f9a8021438b0932b5cc4d37ec36275cbf0ee5c1c08e6a7e99f1f4cccdc` | `6d8dccb582b49135038b55ede52fff1cff88bdf8d31983f1eb61332894e223c0` |
| `shaebani-unger-kertesz-2008-homogeneous-granular-packings-contact-dynamics-pressure-bath` | <https://arxiv.org/pdf/0803.3566v2> | 2026-09-09T07:26:32Z | `2c277872c5b4bfb185cd71e1e1fbec58e64df9a57805f7deeaee04eb6dc4b6f0` | `87e270873bc5cb55431af01bf6a3ed83de1e6faae1591ed7e1201a64a1b086c2` |
| `shojaaee-shaebani-brendel-torok-wolf-2012-parallel-contact-dynamics-domain-decomposition` | <https://arxiv.org/pdf/1104.3516v2> | 2026-09-09T07:31:12Z | `19191f007fa8af3f86e162b268c80a692a5ff0abc8a561237b42b3cc385aed71` | `191168190fc704b69375d1a075b2efa01bf4aeb1a1497e0c50619339ccdc90c9` |
| `skoge-donev-stillinger-torquato-2006-packing-hyperspheres-high-dimensional-euclidean-spaces` | <https://arxiv.org/pdf/cond-mat/0608362v1> | 2026-09-09T07:31:30Z | `d6402c156900ac443afe8e183e4ef8e45797ae8ed94d81a33e083101a0d6492e` | `2c62455b3c065ba1434dd1171fabd8ce363023fe9d06aeafb1d2fa626e0e5af5` |
| `stuyck-chen-2023-diffxpbd` | <https://arxiv.org/pdf/2301.01396v3> | 2026-09-09T07:32:13Z | `04f52ac53eea6f59bb12cfabad23e1531186c33de0b7b515200ebd29816ad445` | `06e75c4f73018b34f0a40d73bbc6880f78a15ffbe500f796a094d60e6b7d1999` |
| `suh-simchowitz-zhang-2022-do-differentiable-simulators-give-better-policy-gradients` | <https://arxiv.org/pdf/2202.00817> | 2026-09-09T07:27:20Z | `53cd097ccd9ccb00b3bf4ef2152a669e01242487de31796e6525034ed68b2c7b` | `5a4dedc28c698c9597dca6cce6e97f8a1be881678056800c83604c94ba664d9e` |
| `torquato-jiao-2009-dense-packings-platonic-archimedean-solids` | <https://arxiv.org/pdf/0908.4107v1> | 2026-09-09T07:25:50Z | `f48afa708aa6d0d2cbf1d56b67aa53e37da7b85dc9253f46f640cf5508065275` | `cbbe10da4e377f0aa6d77f52de9aae4ab4070326ebccff58fbcf954e9b475c13` |
| `torquato-jiao-2009-dense-packings-polyhedra-platonic-archimedean` | <https://arxiv.org/pdf/0909.0940v3> | 2026-09-09T07:25:49Z | `c5628e46cc3cb52d23e5a91e97ec58b50cd2fa7ac6faafbb45d0c7ad88309d20` | `9c9266a6e8fd2c5f8c08afcc144fedba64a9ae0b320a71edb9dc1f551472ecbe` |
| `torquato-jiao-2010-robust-algorithm-sphere-packings-linear-programming` | <https://arxiv.org/pdf/1008.2747v2> | 2026-09-09T07:25:51Z | `eddcae9c381756b15057066949e12cf9c70b35284794ca755aa46a7a8f669df4` | `ad8a8a431c20bbc19f55c20d49a845e32446994826a78d140e195ad2094a2178` |
| `torquato-stillinger-2010-jammed-hard-particle-packings-kepler-bernal` | <https://arxiv.org/pdf/1008.2982v1> | 2026-09-09T07:25:37Z | `243e9953a30205a56dc4727e7d6be26bda3199028cdc954f4eb39947dcaf4423` | `1709fb3200bd2daf10f15d8181b562efa31d23041e3f40df7029836a4ff4c2df` |
| `unger-kertesz-2003-contact-dynamics-method-granular-media` | <https://arxiv.org/pdf/cond-mat/0211696v1> | 2026-09-09T07:26:31Z | `f8f2e45069c71a1fcafd8fa71bfafb551c9030cf6542b9a1552ede8a9c1d4386` | `dea85b8a19dd1dc17444204db5ef65e564720fd4d7bd4a18b0fe674b47dde7a6` |
| `unger-kertesz-wolf-2005-force-indeterminacy-jammed-hard-disks` | <https://arxiv.org/pdf/cond-mat/0403089v3> | 2026-09-09T07:26:36Z | `143e85d8f5ccfa954cbb71f4ed010a3eca4a740ad7eddab29dc66611079b7c11` | `0b798395cf208010abe8136c2d9dc97cc440d6d599952965ed50e7f94e81d47e` |
| `wang-lu-2024-image-space-collage-and-packing-differentiable-rendering` | <https://arxiv.org/pdf/2406.04008> | 2026-09-09T07:27:42Z | `1c10cb5cf84dc0933b11e152c090439fab43b576d6901f3279b6e1acac02ad23` | `f6f36567378872a5d4c2ec15ac5431d855c57078074f263656d7b696b87ebbab` |
| `werling-omens-lee-2021-fast-feature-complete-differentiable-physics` | <https://arxiv.org/pdf/2103.16021> | 2026-09-09T07:27:56Z | `a2ee73c2813366c20d0923037160f089763e46bd317008ece033eae1e5ee4cce` | `d0d13c7aae111efb635a1d5c57159d8e6a48246bb5b85324ec0cf00be69c0ba6` |
| `yaskov-chugay-2020-packing-equal-spheres-block-coordinate-descent` | <https://doi.org/10.32782/cmis/2608-13> | 2026-09-09T07:42:02Z | `1d304d44325520f3117280879b7dc6ae66c789f4773ece6fa6b5e725e2a6ca6a` | `3a583156ab9ca36de69c9ba8e893e388664a3825782d9d7eee752c8c134fe39a` |
| `zhang-lyu-rudra-2026-sequential-object-placement-convex-decomposition` | <https://arxiv.org/pdf/2608.25162v1> | 2026-09-09T07:27:51Z | `3ac52b8353bcae8fe838d4b6f92248dd6c0c2785cbd76d359c19defd84a53ef3` | `d9fce8cead96dd2e9797c954fde8a4d03169765ee00dea9e5d0e8ae3dd293b47` |
| `zhong-han-brikis-2022-differentiable-physics-contacts-correct-gradients` | <https://arxiv.org/pdf/2207.05060> | 2026-09-09T07:27:21Z | `8bd08a87efcdd120d76ca8d3aa8ec7a62b211e74c809d6f42abaf6eeb9f1426a` | `e57104b139316b5e14e3145d217e86925a7a3fa427fc6bed9605dfe9883179e0` |
| `zhou-he-zheng-2023-geometric-batch-optimization-equal-circles` | <https://arxiv.org/pdf/2303.02650v1> | 2026-09-09T07:34:00Z | `66472d71adab27f2b331955adbe2e29c121a4f1b56ddcb909e462ec648de2913` | `fc58b4eaa70995a07fe575183b6fe11ec58fdb67e2cf28128b3126359e5d85d1` |

The single exception to the two-file rule:
`more-wu-1997-global-continuation-distance-geometry.pdf` is a 1998 raster scan with no
text layer. Its faithful extraction is 28 bytes, one form feed per page, and
`pdftotext` emitted no warning at all, which is the failure mode to watch for. An OCR
sidecar is retained beside it, built with `pdftoppm -r 300 -gray -png` and
`tesseract --psm 6`, on the same terms as the Stromquist memoranda already in this
archive: it is a search aid, not source ground truth, and every formula the report
quotes from that source was read off the rendered page images rather than off the OCR.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `more-wu-1997-global-continuation-distance-geometry.ocr.md` | 48134 | `9f95c13c3774e78f1a86065a8aa80de3bff981ba61f00897d8ec619e39286fff` |

One conversion warning was emitted across all 72 extractions, on
`zhang-lyu-rudra-2026-sequential-object-placement-convex-decomposition`, verbatim:
`Syntax Warning: Mismatch between font type and embedded font file`. The extraction is
usable and the PDF is the retained ground truth, as it is for every entry here.

**One download was made and then deleted rather than archived.** A fetch for Stoyan and
Chugay 2014 returned a Cloudflare interstitial with an HTTP 200 status, which was written
to a `.pdf` path before the lane recognised it. The 5,865-byte HTML file was removed. It
is recorded here so the next pass does not read its absence as an untried source: the
source is listed under "attempted and not retrieved" below.

## Readings checked against the retained bytes

The report's most load-bearing readings were verified against these files rather than
against abstracts or against a lane's summary.

- **Gensane and Ryckelynck's own failure mode**, from the already-archived
  `gensane-ryckelynck-2005-improved-dense-packings.raw.md`, read at lines 700 to 760.
  Verbatim: the procedures "seem[] to be 'attracted' by configurations with angle
  `θ = 0` which are rarely good"; and "When the optimal packing for a given `n` contains
  more than two angles as in the case `n = 17`, the chance of finding a good
  approximation of the configuration by procedure `BilliardOfSquares` becomes weak." The
  production calls are on the same page: `BilliardOfSquares(C, 0.1, 10^-8, 1000)` run
  some thousand times on random configurations, then
  `WithPerturbations(C*, 0.1, 10^-12, 1.5, 1000)`. Proposition 1's closed-form inflation
  factor is at line 233 of the same file.
- **Torquato and Jiao's acceptance rule and their justification for the cell move**, from
  `torquato-jiao-2009-dense-packings-polyhedra-platonic-archimedean.raw.md`, section II.
  Verbatim: `p_acc` "with an initial value `p_acc ~ 0.35`, decreasing as a power law with
  exponent equal to `-1` works well for most systems that we studied"; the particle
  motion "is equally likely to be a translation or a rotation"; the ratio of particle
  motions to boundary trial moves "should be greater than unity"; and the strain of the
  fundamental cell "corresponds to non-trivial collective motions of the particle
  centroids ... It is this collective motion that enables the algorithm to explore the
  configuration space more efficiently and to produce highly dense packings."
- **The linear-programming versus Lubachevsky-Stillinger timing table**, read from
  `torquato-jiao-2010-robust-algorithm-sphere-packings-linear-programming.raw.md` around
  line 840: `1.5` hours against `10` minutes in three dimensions, `4.8` hours against
  `46` minutes in four, `14` hours against `3.2` hours in five, and `193.5` hours against
  `8.3` hours in six, at densities agreeing within their stated error bars. The same
  passage supplies the two-step Lubachevsky-Stillinger recipe it compares against, a
  large initial expansion rate of about `0.01` and a fine-tuning rate of `10^-(3+d)`, and
  defines the rattler fraction it reports beside every density.
- **The divide-and-concur disk result**, read from
  `gravel-elser-2008-divide-and-concur.raw.md` around line 231: `n` from 2 to 200, up to
  400 random initial guesses per `n`, "No information about the known packings was used,
  apart from their densities"; 143 of the 197 values reaching within `1e-9` of the best
  known, 38 improved, smallest improved at `n = 91`, largest improvement at `n = 182` at
  `4.6e-5`, and 28 values improved by more than `1e-6`. The metric update
  `lambda_ab -> sigma lambda_ab + (1 - sigma) exp(-alpha d_ab)` with `sigma = 0.99` and
  `alpha` about 30 is on the same page.
- **The relaxed-reflect-reflect settings**, read from
  `elser-2023-how-densely-can-spheres-be-packed-moderate-effort.raw.md` around line 228:
  "fixed-point convergence is fastest when `beta = 1` is used for the RRR time step,
  smaller values are more productive when the search is faced with nonconvex
  constraints. We used `beta = 0.5` in all the experiments", with the metric update rate
  `gamma = 10^-3` except `10^-2` on one hard search.
- **Position-based dynamics' own convergence caveat**, read from
  `muller-heidelberger-hennix-2007-position-based-dynamics.raw.md` around line 289: the
  residual after `n_s` iterations is `delta p (1 - k)^{n_s}`, the substitution
  `k' = 1 - (1 - k)^{1/n_s}` linearises the dependence, "However, the resulting material
  stiffness is still dependent on the time step of the simulation."
- **Nurmela and Ostergard's continuation schedule**, read from
  `nurmela-ostergard-1997-packing-up-to-50-equal-circles-in-a-square.raw.md`, section
  3.2: the energy `(lambda / d_ij^2)^m`, the `sin` reparameterisation that removes the
  container constraint, "We start with a moderately small value of `m` (in the range
  `10 <= m <= 100`) ... Then we double the value of `m` and repeat the optimization
  step", a stopping point "when `m` reaches `10^6`" with `10^50` used in some cases,
  `lambda` reset after each step to the square of the shortest distance, and "For each
  `n`, at least 50 optimization runs were performed with random initial solutions."
- **Maher, Stillinger and Torquato's termination and tolerance**, read from
  `maher-stillinger-torquato-2021-kinetic-frustration-2d-convex-packings.raw.md` around
  line 348: simulations "terminated when `φ` increases less than `10^-10` over the course
  of 100 'random strain' steps", and a contact-generation schedule terminated "when the
  interparticle distances (excluding rattlers) are smaller than `10^-10 D_0` for particle
  shapes composed of arcs and `6 × 10^-10 D_0` for particle shapes containing flat
  edges".

The two claims about squares that the report treats as decisive were checked the same
way. Klement, Lee, Anderson and Engel's statement that event-driven molecular dynamics
for anisotropic particles "requires solving collision equations that involve rotations
and thus trigonometric functions" whose solution "is only possible numerically by
iteration with approximations and is necessarily slow" is in the retained
`klement-engel-2021-newtonian-event-chain-monte-carlo-collision-prediction-polyhedra`.
Jiao, Stillinger and Torquato's statement that they "could not use the DTS algorithm to
study the random jammed packings of particles with extreme shapes, i.e., in the limit
`p → 0.5` and `p → ∞`" is in the retained
`jiao-stillinger-torquato-2010-mrj-packings-superballs`.

## Screened out, and why

The feeds returned a great deal that is adjacent rather than relevant. The dispositions:

| Source or group | Actual subject | Disposition |
| --- | --- | --- |
| Truncated-tetrahedra and superball equilibrium phase-behaviour papers | Three-dimensional phase behaviour under the adaptive shrinking cell, no method contribution | Query receipt only |
| Random sequential adsorption of superballs and superdisks | Irreversible deposition, not a packing optimiser | Query receipt only |
| The hard-square and hard-rectangle density-functional and confinement literature | Equilibrium phase behaviour, not generators | Query receipt only |
| Masonry, asphalt, ballast, tyre and landslide contact-dynamics applications | Process simulation with no density objective | Query receipt only |
| Spurious-elasticity contact-dynamics note | Same content appears in the retained 2003 review | Query receipt only |
| `arXiv:2406.04008`, image-space collage and packing by differentiable rendering | Overlap measured as a pixel count, so exact contact is unavailable by construction | **Retained** as a screened source, cited in the report as screened |
| `arXiv:2504.02465` (shadow-guided packing) and `arXiv:2608.25162` (sequential placement with convex decomposition) | Placement pipelines, not congruent-shape optimal packing | **Retained** as screened sources |
| Iterated dynamic thresholding search 2021; annealing for circle packing 2004 | Same family as the already-retained 2023 thresholding paper | Query receipt only |
| Circle *bin* packing under adaptive annealing | A different objective: many bins, not one minimal container | Query receipt only |
| `arXiv:2405.16618` continuous p-dispersion; `arXiv:1809.10525` circles on a flat torus | Not packing in a bounded square | Query receipt only |
| Two 2026 quasi-physical dynamic papers on circular coverage in convex polygons | Covering, not packing | Query receipt only |
| Douglas-Rachford convergence-theory papers (Aragon Artacho and Borwein; Giladi; Borwein, Lindstrom and Sims; Dizon, Hogan and Lindstrom; Luke, Sabach and Teboulle; Dao, Dressler and Liao; Liao) | Convergence theory, none solving a packing problem | Query receipt only |
| Graduated non-convexity hits across the arXiv sweep | Robust estimation, SLAM and point-cloud registration | Query receipt only; **no source retained and no numeric claim made** |
| "Superdisks in radio galaxies", string-theory "superball" | Homonyms | Query receipt only |

## The zero counts, which are findings

Four searches returned nothing, and each is a negative result the report leans on.

- `all:"position based dynamics" AND all:packing` on arXiv returns **0**, and so does the
  hyphenated variant. `all:"XPBD"` returns 11 papers, none about packing. An OpenAlex
  search for position-based dynamics with packing optimisation returns terrain modelling,
  surgical simulation and pavement-crack sealing.
- `"Douglas-Rachford" AND "packing"` returns **0**.
- `"difference map" AND "packing"` returns **0**.
- `"projection" AND "square packing"` returns **0**.

The report states the consequence: position-based dynamics has never been used as a
packing optimiser, and no projection method has ever been run on polygons in a bounded
container. The one place projection methods *have* been run on packing is under the
divide-and-concur name, which those queries do not match, and which was found through the
author rather than through the phrase.

The literature on the adaptive shrinking cell is small enough to size: an arXiv full-text
search for the exact phrase returns **7** records and OpenAlex returns **27**, of which
the only confinement work is cylindrical.

## Attempted and not retrieved

Nothing below was faked, paraphrased into the archive, or reconstructed. Each was
attempted on 2026-09-09 and each failed for a stated reason. Where the report uses any of
these at all, it says in the sentence that the source was not read.

**A whole host was unreachable, and that is the largest single gap in this pass.** HAL,
which hosts the open copies of the foundational contact-dynamics papers, served an Anubis
proof-of-work challenge page with an HTTP 200 status to every request from this host,
across `hal.science`, `hal.archives-ouvertes.fr`, `hal-lirmm.ccsd.cnrs.fr` and
`hal.umontpellier.fr`. No attempt was made to defeat it.

| Source | Why the report wanted it | Attempt and result |
| --- | --- | --- |
| Moreau 1994, *Some numerical methods in multibody dynamics* | The origin of the contact-dynamics time-stepping scheme | Identified at `hal.science/hal-01789082`; HAL gate. OpenAlex has no DOI record, `oa_status: closed`, one non-open location. **Not read** |
| Jean 1999, *The non-smooth contact dynamics method*, CMAME 177:235 | The canonical statement of the method | Four HAL URLs and mirrors, all HTTP 200 with the challenge page. OpenAlex `closed`, Semantic Scholar green at the same HAL URL. **Not read** |
| Radjai and Richefeu 2009, *Contact dynamics as a nonsmooth discrete element method* | The solver description in its own words | `hal.science/hal-00689866/document`, challenge page. OpenAlex green with HAL as the only open location. **Not read** |
| Radjai, Jean, Moreau and Roux 1996, Phys. Rev. Lett. 77:274 | Force chains under contact dynamics | HAL gate. **Not read** |
| Anitescu and Potra 1997, Nonlinear Dyn. 14:231 | The complementarity formulation | Author page HTTP 403; OpenAlex `closed`, publisher DOI the only location. **Not read** |
| Stewart and Trinkle 1996, IJNME 39:2673 | The other complementarity formulation | Two author pages HTTP 404; OpenAlex `closed`. **Not read** |
| Lubachevsky and Stillinger 1990, *Geometric properties of random disk packings*, J. Stat. Phys. 60:561 | The original inflation paper | OpenAlex on `10.1007/bf01025983`: `is_oa: false`, `oa_status: closed`, `best_oa_location: null`. **Not read.** Everything attributed to it comes from the 1991 Journal of Computational Physics paper's own section 9, from the 2010 review, or from Skoge et al., all retained |
| Lubachevsky, Stillinger and Pinson 1991, J. Stat. Phys. 64:501 | The disks-versus-spheres comparison | Title probe returned `count: 0`; DOI probe on `10.1007/BF01048304` returned `closed`. **Not read** |
| Azema, Radjai and Dubois 2013, *Packings of irregular polyhedral particles*, Phys. Rev. E 87:062203 | Polyhedral contact-dynamics packings | APS PDF HTTP 403. OpenAlex bronze. Substituted with the two retained arXiv papers by the same group |
| Jin and Chan 2020, Phys. Rev. Lett. 124:248002 | Shape-anisotropy ordering under cylindrical confinement | APS only, hybrid, not on arXiv; not fetched after the APS 403 pattern. **Not read, and no claim rests on it** |
| Zhuang, Chen, He, Cao and Wang 2024, *Dynamics simulation-based packing of irregular 3D objects*, Comput. Graph. 123:103996 | A physics-engine packing pipeline | DOI resolves to an Elsevier paywall. OpenAlex `is_oa: false`, `oa_status: closed`, no repository full text. **Not read**; everything about it in the retained 2026 differentiable-packing paper is that paper's characterisation |
| Elser, *Solving Problems with Projections*, Cambridge University Press 2025 | The book-length treatment of relaxed-reflect-reflect and its `beta` guidance | OpenAlex reports bronze open access for chapter 1 only; the chapter URL returned HTTP 200 with an HTML bot wall rather than a PDF. **Not read** |
| Mladenovic, Plastria and Urosevic 2005, Comput. Oper. Res.; and 2007, LNCS | Formulation space search in its own words | Both `closed` on OpenAlex with no open URL. **Not read**; section 8.3 of the report quotes a retained secondary source and says so |
| Liu and collaborators, three energy-landscape-paving papers for circle packing (2009 Comput. Ind. Eng.; 2009 CINC; 2015 Physica A) | The only packing evidence for energy landscape paving | All `closed`, `oa_url: None`. **None read**, and the report records the mechanism as a lead with no packing evidence in hand |
| Stoyan and Yaskov 2004, Eur. J. Oper. Res. | The strip-packing phi-function instances | `closed`. **Not read** |
| Chernov, Stoyan and Romanova 2010 | The original phi-function definition | Nominally bronze; ScienceDirect HTTP 403 and the Wayback capture returns HTML only. **Not read**; the definition used comes from the retained 2018 paper instead |
| Hifi and M'Hallah 2009 | A circle-packing survey | Nominally hybrid; Hindawi and Wiley both HTTP 403, and the Wayback capture is truncated at exactly 1,048,576 bytes with `pdfinfo` failing. Discarded rather than archived corrupt. **Not read** |
| Stoyan and Chugay 2014 | Cuboids with rotations | Hindawi HTTP 403 behind a Cloudflare challenge that returned 200. **Not read**; see the deleted-file note above |
| Baranau and Tallarek 2014, Soft Matter | The measured density-versus-compression-rate curves for Lubachevsky-Stillinger | Not retrieved. The report quotes only the *direction* of the dependence, from the retained review and the public implementation's own README |
| He, Ye and Wang, journal version, Comput. Oper. Res. | Superseded | `closed`; the retained arXiv preprint was read instead |

Two further access notes, recorded so they are not rediscovered. GitHub code search
returns HTTP 401 without authentication; the directory-listing and raw-file endpoints
work and were used instead. The Princeton URL that Skoge et al. give as their code
download, `http://cherrypit.princeton.edu/Packing/C++/`, is dead at DNS.

## What this pass did not cover

- **No search for square-packing *results*.** This pass looked for simulation *methods*.
  Currentness of the record tables belongs to
  [`literature-refresh-2026-09-05`](../literature-refresh-2026-09-05/README.md) and the
  audits beside it, and none was re-run here.
- **No re-run of the 2026-09-08 annealing corpus.** Simulated annealing, basin hopping,
  threshold accepting, replica exchange over a pressure ladder, iterated tabu search and
  perturbation-based thresholding search were deliberately out of scope, and the two
  paywalled replica-exchange papers that pass could not obtain were not attempted again.
- **No citation-chain expansion.** The works citing Torquato and Jiao 2009, or citing
  Gravel and Elser 2008, were not enumerated beyond one OpenAlex citation probe on the
  2010 divide-and-concur paper.
- **No replay of anything retained.** Every number in the report is read from a retained
  source or from this repository's own registers. No mechanism was implemented and no run
  was made.
- **No proof-of-work or bot-wall circumvention**, which is why the four foundational
  contact-dynamics papers are missing.
- **No Google Scholar or DBLP.** Four indexes were queried: arXiv, Crossref, OpenAlex and
  Semantic Scholar.
- **No licence review of the implementations named**, beyond reading the licence field
  that each repository's own API returns. Two of the named projects declare no licence at
  all, which the report notes and which anyone vendoring them would have to resolve.
