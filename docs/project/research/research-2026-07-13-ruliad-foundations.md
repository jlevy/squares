---
title: Research Brief on Stephen Wolfram's Ruliad
description: An evidence-ranked assessment of the Ruliad's formal construction, observer theory, physical claims, mathematical claims, and open problems
author: OpenAI Codex
---

# Research: Stephen Wolfram's Ruliad

**Date:** 2026-07-13 (last updated 2026-07-14)

**Author:** OpenAI Codex

**Status:** Complete

## Executive Summary

Stephen Wolfram defines the **Ruliad** as the limiting structure obtained by running every possible computational rule, from every possible initial condition, in every possible way, for arbitrarily many steps, while identifying equivalent states. The word “entangled” refers first to the merging of computational histories that arrive at equivalent states. Wolfram then interprets this total computational structure as the common substrate of physics, mathematics, and computation.

The 2021 essay develops three connected proposals:

1. **A formal proposal:** Multiway rewriting systems can represent nondeterministic computations, physical update histories, and formal proofs. A “rulial” multiway system expands this construction across rules; the Ruliad is its all-rules, all-resources limit.
2. **An observer proposal:** Computationally bounded, persistent observers cannot resolve the full structure. They coarse-grain it by treating many states and histories as equivalent. Wolfram argues that general relativity, quantum mechanics, and thermodynamics emerge generically from this restricted perspective.
3. **An ontological proposal:** The Ruliad is not merely a model. It is the uniquely necessary totality of everything computationally possible, and our physical universe is an observer-dependent slice of it.

These layers have different evidential status. The finite rewriting constructions and their connections to proof theory, graph rewriting, computation, and higher categories are mathematically substantive. Several conditional results about discrete covariance, continuum limits, causal sets, and homotopy types have been published. The uniqueness of the full Ruliad, the claimed generic derivation of known physics from observers, and the identification of the Ruliad with reality remain conjectural. The final claim is metaphysical unless it is connected to discriminating empirical predictions.

The most defensible interpretation is therefore not “a completed theory of everything.” It is a broad research program that combines:

- exhaustive exploration of simple rules
- nondeterministic and higher-dimensional rewriting
- observer-dependent coarse-graining
- geometric study of computation and proof
- discrete approaches to spacetime and quantum foundations

This program could become useful even if its strongest ontological claims are false. Its best prospects are as a computational laboratory for discrete physics, a geometry of proof and program space, and a framework for studying how bounded observers extract stable laws from complicated processes. It does not currently replace set theory, type theory, quantum field theory, general relativity, or the Standard Model.

## Questions Answered

1. What is the Ruliad, and how does Wolfram construct it?
2. How does the argument connect computation, observers, physics, and mathematics?
3. Which claims are definitions or established formal results, and which are conjectures or metaphysics?
4. How does the proposal relate to existing work in logic, computer science, quantum gravity, and philosophy?
5. What are the strongest criticisms and alternative interpretations?
6. What would have to be proved or observed for the program to affect the foundations of mathematics or physics?

## Scope

The primary source is Wolfram's full 2021 essay, [The Concept of the Ruliad](https://writings.stephenwolfram.com/2021/11/the-concept-of-the-ruliad/). Supporting sources cover the 2020 Wolfram Physics Project, the 2022 metamathematics program, published mathematical work on multiway rewriting and homotopy types, subsequent work on observers, and Wolfram's extensions through July 2026.

The practical question is whether the Ruliad should be treated as a mathematical formalism, a physical theory, a metamathematical research program, or an ontology. The analysis evaluates conceptual and formal claims; it does not reproduce the large computational experiments in Wolfram Language or audit every proof in the companion technical papers.

For Chaitin's algorithmic information theory and halting probability, see the
[Chaitin research report](research-2026-07-13-gregory-chaitin-ait-omega-metabiology.md).
Their direct intersection with quantum observation, black holes, and physical
undecidability is assessed in the
[foundations-of-physics report](research-2026-07-14-chaitin-ruliad-foundations-physics.md).

## Development of the Program

The Ruliad is the unifying layer of a program that has continued to expand:

- **2020:** The Wolfram Physics Project introduced local hypergraph rewriting, multiway evolution, causal invariance, and proposed correspondences with relativity and quantum mechanics.
- **2021:** The Ruliad essay generalized from a search for one physical rule to the all-rules limit and made observer-dependent sampling central.
- **2022:** The metamathematics project treated formal theories and proofs as physicalized multiway structures. Companion work developed higher homotopies in rewriting systems.
- **2023:** Wolfram's observer theory and the philosophical Ruliology paper made bounded observers, sampling, and the reconstruction problem more explicit.
- **2024:** The journal version of the pregeometry work gave a more precise category-theoretic construction of Rulial space and stated extra conditions required for topology and smooth geometry.
- **2025:** Work on a generalized theory of observers began formalizing minimal observers, equivalence, and complexity. Wolfram also extended Rulial ideas to biology and minds.
- **2026:** Wolfram recast the empirical study of rule spaces as “ruliology,” applied it to the P versus NP problem, and presented the Ruliad as the basis of a proposed scientific metaphysics. P versus NP asks whether every efficiently checkable solution is also efficiently findable.

This growth shows that the Ruliad is an active umbrella program rather than a single finished paper. It broadens the range of applications, but breadth is not independent confirmation of the central physical and ontological claims.

## The Core Construction

### Multiway Systems

Start with a state and one or more rewrite rules. Instead of selecting a single applicable update, apply every applicable update. The resulting directed graph is a **multiway graph**:

- vertices are states
- edges are rule applications
- branches represent different possible update histories
- branches merge when their resulting states are treated as equivalent

For strings, equivalence may be literal string equality. For hypergraphs, it is usually graph isomorphism. This equivalence relation is essential: without merging, the structure is just a tree of separately labeled histories. With merging, histories become connected by shared outcomes.

An ordinary multiway system uses a fixed rule set. A **rulial multiway system** also ranges over different rules. Wolfram's finite examples use bounded families such as short string substitutions, small Turing machines, or small hypergraph replacement rules.

### The Infinite Limit

The proposed Ruliad takes several limits at once:

- all computational rules
- all initial conditions
- all allowed rule applications
- unbounded computation time
- unbounded state or memory size
- unbounded rule-description length

Wolfram describes this as the “entangled limit of all possible computations.” In computation-theoretic terms, it is an attempt to let time complexity, space complexity, and program-size complexity all tend to infinity.

The phrase is evocative, but it is not yet a complete mathematical definition. A rigorous definition must specify:

- the computational basis and encoding
- the equivalence relation on states, rules, and histories
- whether edges retain labels identifying the rules used
- the order or directed system used to take the limits
- the topology, metric, or categorical notion of convergence
- a measure, if claims such as “almost all rules” or observer typicality are made

Wolfram acknowledges in the essay that these technical details and the handling of the infinite limits remain unfinished.

### Why Wolfram Thinks the Limit Is Unique

Standard models of effective computation can encode one another, as summarized in the literature on the [Church–Turing thesis](https://plato.stanford.edu/entries/church-turing/). Wolfram appeals to the stronger **Principle of Computational Equivalence** (PCE), which says, roughly, that systems whose behavior is not obviously simple tend to attain the same maximal level of computational sophistication. He uses PCE to support two claims:

1. A Ruliad built from Turing machines, cellular automata, combinators, or hypergraph rewriting should ultimately be the same object in different coordinates.
2. The Ruliad should be broadly homogeneous because most sufficiently sophisticated regions can emulate one another.

Universal computation supports mutual simulation. It does not by itself establish these stronger geometric conclusions. Two universal formalisms may compute the same partial functions while differing greatly in local graph structure, simulation overhead, locality, and resource complexity. PCE is a research principle supported by examples, not a theorem comparable to the formal equivalence of standard models of computability. The difference matters because Wolfram needs more than computability equivalence: he needs enough metric or large-scale equivalence to obtain one observer-independent limiting geometry.

## How Observers Enter

The full Ruliad includes every computable history. Yet we experience definite events and stable laws. Wolfram's answer is that we are embedded, computationally bounded observers.

An observer in this framework:

- occupies only a tiny part of the total computation
- has limited memory and processing capacity
- persists sufficiently to treat itself as the same observer over time
- compresses microscopic detail into equivalence classes
- experiences a sequence because it cannot shortcut computationally irreducible evolution

The gas analogy is central. A pressure gauge ignores molecular trajectories and records an aggregate variable. Likewise, Wolfram proposes that observers ignore most microscopic rule applications and perceive robust macroscopic regularities. The laws are then properties of the relationship between substrate and observer, not of the substrate alone.

This is the conceptual engine of the entire proposal. It also creates its main explanatory burden. “Computationally bounded” and “persistent” describe a large range of possible systems. To derive physics, the theory needs a precise class of observer maps or coarse-grainings, plus a proof that almost every observer in that class perceives the claimed laws. Otherwise the observer can function as a flexible selector that extracts the desired behavior after the fact.

## Physical, Branchial, and Rulial Space

Wolfram uses three related geometries.

### Physical Space

In the Wolfram model, a hypergraph represents elementary spatial relations. Repeated local rewrite events generate a causal graph. Familiar spatial geometry is supposed to arise as a large-scale limit of the hypergraph.

### Branchial Space

A fixed rule can have many possible update histories. A time slice across the multiway graph groups states by their branching relationships. States with recent common ancestry are close in **branchial space**. Wolfram associates this geometry with quantum entanglement and treats a bounded observer as conflating many branches into one experienced history.

### Rulial Space

Rulial space also separates histories generated by different rules. Distance is interpreted as the computational cost of translating or emulating one rule in another. Different programming languages, models, and conceptual schemes are treated as locations or reference frames in rulial space.

This yields suggestive analogies:

- light cones in physical space
- entanglement cones in branchial space
- emulation cones in rulial space
- particles as persistent structures in physical space
- concepts as persistent, communicable structures in rulial space

The first three can be given formal graph meanings in specific models. The claims about minds, concepts, paradigm shifts, or alien civilizations are exploratory interpretations, not established consequences.

## The Physics Claim

### General Relativity

The Wolfram Physics Project uses **causal invariance**: different permissible orders of local updates must yield the same causal structure. In a technical companion paper, Jonathan Gorard relates this to discrete general covariance and derives discrete curvature constructions and Einstein-like constraints under assumptions that include an appropriate continuum limit and asymptotic dimension preservation. See [Some Relativistic and Gravitational Properties of the Wolfram Model](https://arxiv.org/abs/2004.14810).

This is meaningful mathematical work, but its logical form is conditional. If a rewrite system has the required causal invariance, dimensional behavior, and continuum properties, then familiar relativistic structures can emerge. It does not show that a generic simple rule has those properties, that our universe follows such a rule, or that the Ruliad uniquely selects the observed solution and matter content.

The relationship to **causal set theory** is particularly close. Causal set theory also posits a discrete causal order from which continuum spacetime should emerge. A [Living Reviews overview](https://link.springer.com/article/10.1007/s41114-019-0023-1) describes the mature causal-set program and its reconstruction problems. Work on [algorithmic causal sets and the Wolfram model](https://arxiv.org/abs/2011.12174) shows that hypergraph rewriting can supply an algorithmic dynamics for certain causal-set constructions.

### Quantum Mechanics

Multiway branching supplies a natural resemblance to sums over histories. Gorard's published [Some Quantum Mechanical Properties of the Wolfram Model](https://doi.org/10.25088/ComplexSystems.29.2.537) develops correspondences with projective Hilbert-space geometry, a multiway Born rule based on path weights, Bell-inequality violation, the path integral, and a discrete Schrödinger equation.

Again, the distinction between representation and empirical derivation is important. A general graph formalism can encode quantum structures. A fundamental physical theory must also explain why the relevant weights are the observed complex amplitudes, why evolution preserves total quantum probability and information (unitarity), why the Born probabilities apply, and how relativistic quantum field theory, chiral fermions, gauge symmetries, renormalization, and the Standard Model emerge together from the same microscopic dynamics.

The Ruliad essay often says that general relativity and quantum mechanics are “inevitable” for observers like us. The sources reviewed do not yet provide a theorem with a precise observer class whose conclusion is the full empirical content of either theory. They provide structural analogies, formal embeddings, and conditional continuum results.

### Thermodynamics

The observer argument is most plausible for thermodynamics. Coarse-grained observers normally lose information about microscopic states, making entropy increase typical relative to their macroscopic variables. This resembles standard statistical mechanics and information-theoretic accounts of the arrow of time.

The remaining foundational questions are familiar ones: which measure defines typical microstates, why the universe had a low-entropy past, and why the observer's coarse-graining is physically privileged. The Ruliad reframes these questions but does not automatically answer them.

### Empirical Status

The 2020 core paper is deliberately titled [A Class of Models with the Potential to Represent Fundamental Physics](https://arxiv.org/abs/2004.08210). That cautious title is a good description of the current status.

The project has produced published and preprint work on relativity, quantum formalism, causal sets, numerical relativity, higher categories, and rewriting. However, in the sources reviewed through 2026-07-13, I found no public derivation from the Ruliad of:

- the observed particle spectrum and gauge group
- the values of particle masses or dimensionless couplings
- a unique microscopic rule or well-defined ensemble for our universe
- a novel quantitative prediction that distinguishes the framework from established physics

The project offers some rough scale estimates, but these depend on substantial assumptions. In 2020, physicists quoted by [Scientific American](https://www.scientificamerican.com/article/physicists-criticize-stephen-wolframs-theory-of-everything/) criticized the results as qualitative and insufficiently predictive. That article predates later technical papers, so it should not be treated as the last word. Its central empirical challenge remains unanswered.

## The Mathematics Claim

### Formal Theories as Multiway Systems

A formal theory can be represented as a graph:

- states are expressions, propositions, proof states, or contexts
- axioms and inference rules are rewrites
- proofs are paths
- theorems are reachable states
- proof equivalences become higher-dimensional identifications between paths

This is compatible with established proof theory, term rewriting, automated theorem proving, categorical logic, and the Curry–Howard view of proofs as structured objects. Wolfram's distinctive move is to treat the large-scale geometry of all such proof processes as something that can be studied empirically, much as statistical mechanics studies the large-scale behavior of many microscopic interactions.

A **mathematical observer** is then a mathematician, proof assistant, or other bounded system that identifies many low-level derivations as “the same idea.” Human mathematics operates at the level of groups, manifolds, functors, or invariants, not raw symbol substitutions. Wolfram compares this to fluid mechanics emerging above molecular dynamics.

This is a strong and useful insight even without the full Ruliad. Proof corpora and proof-assistant traces can be analyzed for:

- clusters of concepts
- distances between theorems
- reusable lemmas and bottlenecks
- alternative proof paths
- phase transitions in proof-search difficulty
- compression into human-understandable abstractions

Wolfram's 2022 [Physicalization of Metamathematics](https://arxiv.org/abs/2204.05123) develops this program and argues that human mathematics is an observer-dependent sampling of the Ruliad.

### Higher Categories and Homotopy Types

When rewrites are treated as morphisms, equivalences between rewrite paths behave like 2-morphisms; equivalences between those equivalences continue to higher levels. This connects multiway systems with higher categories, homotopy type theory, polygraphs, and rewriting modulo higher relations.

The connection has been formalized for specified constructions. [Homotopies in Multiway Rewriting Systems as n-Fold Categories](https://arxiv.org/abs/2105.10822) constructs higher homotopies and obtains an infinity-groupoid after adding appropriate inverse relations. [Pregeometric Spaces from Wolfram Model Rewriting Systems as Homotopy Types](https://link.springer.com/article/10.1007/s10773-024-05576-0) gives a more precise category-theoretic treatment and identifies additional conditions needed to obtain topology and geometry.

The qualification is important. Grothendieck's homotopy hypothesis says, in broad terms, that infinity-groupoids model homotopy types. It does not say that every all-rules rewrite graph automatically becomes a unique smooth physical spacetime. Moving from a higher groupoid to a manifold with the geometry and dynamics of our universe requires extra structure such as locality, cohesivity, a metric notion, a continuum limit, and selected sections or projections. The later technical paper is more careful about these conditions than the broad wording of the 2021 essay.

### Does This Replace Axiomatic Foundations?

No, not in its present form.

Set theory, type theory, categorical foundations, and proof theory provide languages for stating consistency, interpretation, construction, and proof. The Ruliad itself must be defined in some metatheory. Calling it “below axioms” does not remove that dependence; it moves attention from a chosen object-level axiom system to a meta-level enumeration of rules and equivalences.

There is also a truth-versus-reachability issue. An all-rules graph contains consistent and inconsistent axiom systems, different logics, and arbitrary symbol transformations. To function as a foundation of mathematics, it must preserve the context that identifies which theory and inference rules license a path. Otherwise unrestricted mixing of rules makes reachability nearly trivial. Classical inconsistency also causes explosion inside an inconsistent theory. Observer selection can recover the mathematics humans use, but then the foundational work is being done by the definition of the observer and its admissible equivalences.

The promising contribution is therefore a **metamathematical science of formal systems**, not yet a replacement foundation.

## The Computation-Theory Claim

The Ruliad geometrizes familiar questions:

- a computation is a path
- a universal interpreter is a translation between regions
- halting systems resemble terminal regions or “black holes”
- undecidability appears as the possibility of unbounded paths
- Chaitin's Omega represents a noncomputable measure of halting behavior for a chosen universal machine
- P versus NP is pictured as a question about how deterministic paths fill or fail to fill a larger nondeterministic region

These pictures can generate intuition, but geometric restatement is not resolution. In his 2026 essay [P vs. NP and the Difficulty of Computation](https://writings.stephenwolfram.com/2026/01/p-vs-np-and-the-difficulty-of-computation-a-ruliological-approach/), Wolfram reports empirical exploration and expresses doubt that the general question will yield to a finite conventional proof. He does not prove P = NP, P ≠ NP, or independence from standard axioms.

The most productive computational direction is likely systematic **ruliology**, which Wolfram now defines as the empirical and theoretical study of what simple rules do. This is a legitimate research activity regardless of whether the Ruliad is physically real. Its subjects include universality, simulation overhead, rule-space phase diagrams, computational irreducibility, and the discovery of useful algorithms.

## Claim-by-Claim Assessment

| Claim                                                                                                        | Status                                                      | Assessment                                             |
| ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- | ------------------------------------------------------ |
| Fixed rewrite systems generate multiway graphs                                                               | Definition and established formalism                        | Solid                                                  |
| Formal theories and proof searches can be encoded as multiway systems                                        | Established in rewriting and proof theory                   | Solid, though not unique to this program               |
| Selected multiway systems support higher categorical and homotopical constructions                           | Published mathematical results under stated constructions   | Substantive and promising                              |
| Causal invariance yields discrete covariance and Einstein-like continuum constraints                         | Conditional technical results                               | Interesting, but assumptions do significant work       |
| Quantum structures can be represented through branchial graphs                                               | Published formal correspondences                            | Interesting; empirical completeness is not established |
| All computational bases converge to one unique Ruliad                                                        | Conjecture requiring a precise limit and invariance theorem | Open                                                   |
| Most sophisticated computations are equivalent in the sense needed for Rulial geometry                       | PCE, a broad research principle                             | Open and measure-dependent                             |
| Bounded, persistent observers generically perceive general relativity, quantum mechanics, and the second law | Central conjecture                                          | Not established at the level claimed                   |
| The Ruliad is everything that physically exists                                                              | Ontological thesis                                          | Metaphysical without additional empirical linkage      |
| The Ruliad is a new foundation replacing axiomatic mathematics                                               | Programmatic thesis                                         | Not currently justified                                |

## Related Work and Intellectual Context

### Computability and Universal Simulation

The Ruliad belongs to the tradition of Turing's universal machine and the Church–Turing thesis. The [Stanford Encyclopedia entry](https://plato.stanford.edu/entries/church-turing/) stresses that the original thesis concerns effective methods. Claims about all physical processes or efficient simulation are stronger theses. Wolfram's PCE is stronger again: it suggests a widespread equivalence of computational sophistication in natural and abstract systems.

Jürgen Schmidhuber's [Algorithmic Theories of Everything](https://arxiv.org/abs/quant-ph/0011122) also studies ensembles generated by all computable descriptions, but adds algorithmic probability and speed-based priors. That difference is important. A totality of all programs does not predict observations until it assigns weights or a selection rule. Algorithmic probability supplies one candidate, although it remains reference-machine dependent up to invariance bounds and is generally uncomputable.

### Mathematical and Modal Totalities

Max Tegmark's [Mathematical Universe Hypothesis](https://arxiv.org/abs/0704.0646) proposes that physical reality is a mathematical structure and considers an ensemble of mathematical structures. The Ruliad is narrower in one way, because it centers computable rule systems, and more connected in another, because different computations can merge and emulate one another rather than existing as a bare catalog of separate universes.

The proposal also resembles:

- Leibniz's monads and possible worlds
- David Lewis's modal realism
- Borges's library of all possible books
- Everettian branching
- Kant's distinction between an underlying reality and the observer-conditioned form of experience

The Kantian comparison is especially useful. The Ruliad plays the role of an observer-independent totality, while computational boundedness and persistence play the role of conditions that shape experience. The missing analogue of Kant's deduction is a proof that these observer conditions uniquely or generically yield our physics.

### Discrete Quantum Gravity

The Wolfram model is part of a larger family of programs in which continuum spacetime is emergent:

- causal set theory
- loop quantum gravity and spin foams
- causal dynamical triangulations
- tensor-network and quantum-information approaches
- quantum cellular automata
- graph and hypergraph rewriting

Its distinctive ingredients are executable local hypergraph rules, explicit multiway evolution, and the attempt to unify different rules through Rulial space. The reconstruction problem is shared: how does one recover smooth Lorentzian spacetime, quantum field theory, matter, and observed constants from non-spatiotemporal microscopic structures?

### Categorical and Rewriting Approaches

The higher-category work connects naturally to:

- term and graph rewriting
- Knuth–Bendix completion and confluence
- polygraphs and higher-dimensional rewriting
- homotopy type theory and univalence
- categorical quantum mechanics and the ZX calculus, a graphical language for quantum processes

These connections are among the strongest parts of the program because they yield precise constructions and reusable mathematical tools. They do not depend on accepting the Ruliad as an ontology.

### Observer-Centered Approaches

Observer dependence has precedents in statistical mechanics, relativity, operational quantum theory, cybernetics, Bayesian inference, relational quantum mechanics, and renormalization. Constructor theory is another meta-level program that starts with possible and impossible transformations rather than a single dynamical law.

[Ruliology: Linking Computation, Observers and Physical Law](https://arxiv.org/abs/2308.16068) gives a sympathetic philosophical analysis but identifies a “realization” or reconstruction problem: an abstract rule does not by itself explain physical actuality. It ultimately interprets the Ruliad as a pre-physical framework and a home for possible theories, rather than an ordinary predictive physical theory. A later paper, [Towards a Generalized Theory of Observers](https://arxiv.org/abs/2504.16225), begins formalizing observer equivalence and complexity. This is exactly the area that needs further development.

## Main Criticisms

### 1. The Full Ruliad Is Not Yet Well Defined

Finite approximations are clear. The simultaneous infinite limit is not. Different enumerations, encodings, state equivalences, and growth schedules can produce different local and asymptotic structures. Mutual computability does not prove graph isomorphism, large-scale distance preservation (quasi-isometry), measure equivalence, or the preservation of continuum observables.

The phrase “all possible rules” also requires a syntax. There is no uniform probability distribution over a countably infinite collection of finite programs: assigning each program the same positive mass makes the total diverge, while assigning zero to each makes the total zero. Any statement about “most” rules therefore needs a size cutoff, a reference language, or an algorithmic prior.

### 2. Universality Is Weaker Than Rulial Relativity

A universal system can simulate another system, but the simulation may be slow, nonlocal, or geometrically distorted. Physics depends on locality, causal structure, symmetry, and resource scaling, not just on which functions are computable. A proof of Rulial relativity would need robust bounds on simulation overhead and a demonstrated invariant large-scale geometry.

### 3. The Observer May Be Doing Too Much

If the observer chooses the equivalence relation, time slicing, description language, and relevant variables, it can potentially extract many incompatible effective theories from the same totality. The framework needs:

- a formal class of admissible observers
- a non-circular account of persistence and identity
- a measure or typicality principle over observers
- a theorem showing that the observed laws are generic in that class
- an explanation of why observers agree on quantitative facts

Without these, “observers like us see physics like ours” risks becoming close to a restatement rather than an explanation.

### 4. Structural Recovery Is Not Quantitative Physics

Recovering covariance, a Hilbert-space metric, or an Einstein-like equation is not the same as reproducing the measured world. A successful fundamental theory must recover the specific low-energy effective field theory, matter representations, anomaly cancellation, dimensionality, constants, cosmological history, and precision tests already explained by existing theories.

The strongest fair criticism is not that the mathematical analogies are empty. It is that the distance from those analogies to quantitative physics is much larger than the project's broad presentations sometimes imply.

### 5. “Everything Exists” Moves the Selection Problem

The Ruliad answers “why this rule?” with “all rules.” It then has to explain:

- why our observations correspond to this region or equivalence class
- why observers like us are typical or expected
- why the measured regularities have these probabilities
- why the underlying category is computation rather than a broader noncomputable structure

Wolfram addresses the last question by asserting that we are computational, not hypercomputational, observers. This is a plausible physical hypothesis, but it is not a formal necessity. The [Church–Turing literature](https://plato.stanford.edu/entries/church-turing/) distinguishes effective computability from stronger claims about what physical reality can do.

### 6. Abstract Existence Does Not Establish Physical Actuality

An abstract totality can be defined without showing that it is physically instantiated. The move from “the Ruliad exists as a formal construction” to “the Ruliad is everything that exists” is philosophical. Calling the structure necessary does not by itself breathe physical content into it.

This does not make the thesis meaningless. It places it alongside structural realism, mathematical Platonism, modal realism, and other ontologies whose evaluation is partly philosophical until they alter empirical expectations.

### 7. The Mathematical Foundation Still Needs a Metatheory

To define rules, graphs, limits, equivalence, and observers, the theory uses mathematics. It therefore cannot straightforwardly ground all mathematics without addressing self-reference and the metatheory in which the grounding is formulated. Gödelian incompleteness and undecidability are represented inside the Ruliad, but representing them does not remove them.

### 8. Falsifiability Is Unclear at the Ruliad Level

A framework containing every computable model is compatible with every computable observation unless it supplies restrictions on which observers see which outcomes and with what probability. The finite Wolfram models can be tested mathematically. A candidate physical rule can be tested empirically. The bare all-rules totality is difficult to falsify.

This suggests a useful separation:

- **Ruliology:** a testable mathematical and computational science of rule spaces
- **Wolfram-model physics:** a potentially testable class of discrete physical models
- **Ruliad ontology:** a philosophical interpretation of the totality

Conflating these three makes both praise and criticism less precise.

## Alternative Interpretations

### Literal Computational Ontology

Everything that exists is the Ruliad; physical and mathematical worlds are observer-dependent samplings. This is Wolfram's strongest interpretation and the least empirically constrained.

### Pre-Physical Framework

The Ruliad is a space of possible theories, and physics is the task of locating the observer-compatible region describing our observations. This is the interpretation favored in the 2023 philosophical paper. It is coherent, but a space containing all models is not by itself a physical explanation.

### Geometry of Computation and Proof

The Ruliad is an aspirational name for a universal atlas of programs, simulations, formal systems, and translations. This interpretation retains most of the mathematical and computer-science value while dropping the claim that formal possibility is physical actuality.

### Theory of Observer-Dependent Effective Laws

The central subject is not the totality but the map from microscopic computational processes to the macroscopic invariants accessible to bounded observers. On this reading, the Ruliad motivates a generalized theory of coarse-graining, renormalization, and representation.

### Generative Metaphor

Terms such as Rulial particles, Rulial gravity, motion between minds, and Rulial aliens can be read as hypothesis-generating metaphors. They should not be treated as results until operational definitions support them.

The third and fourth interpretations are currently the strongest scientifically.

## Future Relevance

### Foundations of Mathematics

The program could matter through **empirical metamathematics** rather than by replacing axioms.

Promising directions include:

- building large proof graphs from Lean, Coq, Isabelle, Metamath, and other formal libraries
- measuring theorem distance, proof curvature, bottlenecks, and community structure
- studying how different foundations translate or fail to translate into one another
- detecting high-level concepts as stable compression structures across proof corpora
- modeling human and machine mathematicians as different bounded observers
- turning machine-found proofs into explanations at a useful level of abstraction
- studying how axiom choices change the navigable geometry of mathematical practice
- using higher rewriting and homotopy types to organize proof identity

This could inform the philosophy of whether mathematics is discovered or invented. The formal rule space is “there” once specified, while the mathematics humans practice depends on observer interests, notation, compression, and cognitive constraints. That is a plausible middle position between unqualified Platonism and pure formalism.

The hard requirement is to demonstrate new theorems, proof-search methods, interoperability, or explanatory tools that outperform existing approaches.

### Foundations of Physics

The most relevant research questions are concrete:

- Which local hypergraph rules have stable dimension and a controlled continuum limit?
- Can causal invariance be classified or efficiently tested?
- Which universality classes yield Lorentzian geometry?
- Can the same microscopic model yield unitary quantum theory and relativistic causal structure?
- How do chiral fermions, gauge fields, and anomaly cancellation arise?
- Can the model recover quantum field theory and the Standard Model without inserting their structure?
- Is there a principled measure over rules or histories?
- Can any observed constant be calculated?
- Does the model predict a deviation in black-hole physics, cosmology, particle physics, or quantum experiments?

Even negative answers would be useful. Hypergraph rewriting can serve as a laboratory for the reconstruction problem in quantum gravity and as a bridge between causal sets, discrete geometry, rewriting theory, and numerical relativity.

### Foundations of Computation

Ruliology can contribute by studying the distribution, geometry, and translation cost of computations:

- empirical universality thresholds
- minimal universal machines
- compiler and interpreter overhead as a metric
- phase diagrams of decidability and halting behavior
- computational irreducibility in ensembles
- average-case behavior across rule classes
- geometric reformulations of complexity classes
- automated discovery of useful programs

This work must use carefully specified ensembles. Results for a finite enumeration do not automatically generalize to an invariant “space of all programs.”

### Artificial Intelligence and Scientific Understanding

AI systems make the observer idea more operational. Different models compress the same data into different internal representations. Research could ask which concepts remain stable across architectures, training histories, formal languages, and proof systems.

Potential applications include:

- machine-generated conceptual translations
- detecting shared abstractions across scientific fields
- estimating Rulial distance through translation or simulation cost
- evaluating when two models are behaviorally equivalent
- studying the boundary between a proof and an understandable explanation

These are testable research questions. Claims that concepts are literal particles in Rulial space are not yet needed.

### Other Open Questions

The Ruliad provides a common vocabulary for several foundational problems, but mostly reframes them:

- **Why these laws?** All laws exist; observer location and typicality become the new problem.
- **Why quantum mechanics?** Multiway histories supply branching; amplitudes, probability, and measurement still require detailed derivation.
- **Why an arrow of time?** Irreducible computation plus coarse-graining supplies a direction; the low-entropy boundary condition remains.
- **Why is mathematics effective in physics?** Both are observer samplings of the same formal substrate; this is an elegant explanation if the common substrate thesis is established.
- **What is consciousness?** Bounded coherent observers are modeled functionally, but subjective experience is not explained.
- **What is extraterrestrial intelligence?** Rulial distance offers a metaphor for radically different representations, but currently gives no method for detecting extraterrestrial intelligence.
- **Can P versus NP be solved geometrically?** Rulial pictures may guide empirical exploration but have not resolved the problem.

## What Would Change the Assessment

The program would become a serious candidate foundation if it achieved several milestones.

### Formal Milestones

1. Give a precise construction of the Ruliad as a limit in a specified category.
2. Prove invariance, or a suitably weaker quasi-isometry or universality result, across computational bases.
3. Define a non-arbitrary topology and measure on rule, state, and observer space.
4. Separate rule syntax, theory context, derivability, semantic truth, and physical realization.

### Observer Milestones

1. Define bounded observers as explicit computational maps or subsystems.
2. Derive persistence rather than assuming it only in the cases of interest.
3. Prove that a broad, independently motivated observer class sees the claimed invariants.
4. Derive agreement, probabilities, and typicality across observers.

### Physics Milestones

1. Identify a candidate rule or well-defined ensemble before fitting new data.
2. Recover known low-energy physics quantitatively.
3. Calculate at least one dimensionless observed quantity not used as input.
4. Produce a novel, risky prediction that competing frameworks do not share.
5. Obtain independent replication and comparison with established quantum-gravity approaches.

### Disconfirming Outcomes

The strongest claims would be weakened if:

- different universal bases yield inequivalent large-scale Rulial geometries
- the desired laws appear only for specially chosen observer equivalences
- no single rule or principled ensemble recovers relativistic quantum field theory
- the framework remains compatible with every observation but predicts none
- categorical or continuum results require inserting the target physical structure as an assumption

## Recommendations

Evaluate the program as three related layers with different standards of success:

1. **Ruliology and multiway mathematics:** Judge these by new theorems, algorithms, classifications, and useful proof-space or rule-space tools.
2. **Wolfram-model physics:** Judge this layer by quantitative recovery of established physics and novel, independently testable predictions.
3. **Ruliad ontology:** Treat the identification of the Ruliad with reality as a philosophical interpretation unless it changes empirical expectations.

Near-term work should prioritize a basis-invariant definition of the limit, a formal theory and measure of admissible observers, interoperable proof-space tools, and a preregistered physical prediction. This separation preserves the program's useful mathematics without treating mutual computability as a proof of geometric uniqueness or treating formal possibility as physical actuality.

The Ruliad merits study as an exploratory framework with promising technical branches. The available evidence does not yet support treating it as an established foundation for mathematics or a confirmed theory of nature.

## Methodology

The complete 2021 essay was read section by section, including its construction, observer theory, mathematics and computation sections, hypercomputation discussion, physics claims, philosophical implications, and multiplicative toy example. The review then cross-checked:

- Wolfram's core and subsequent essays through July 2026
- technical papers on relativity, quantum mechanics, causal sets, rewriting, and higher categories
- philosophy-of-science work on observers and the realization problem
- antecedents in computability, algorithmic ensembles, mathematical structuralism, and discrete quantum gravity
- contemporary criticism focused on prediction, circularity, and formal precision

Priority was given to primary papers, journal versions, authoritative reviews, and commentary identified as such. Claims of absence, such as the lack of a quantitative prediction, refer to the public sources reviewed and should be revisited if the project publishes new results.

## References

### Primary Wolfram Sources

- Stephen Wolfram, [The Concept of the Ruliad](https://writings.stephenwolfram.com/2021/11/the-concept-of-the-ruliad/) (2021)
- Stephen Wolfram, [A Class of Models with the Potential to Represent Fundamental Physics](https://arxiv.org/abs/2004.08210) (2020)
- Stephen Wolfram, [The Physicalization of Metamathematics and Its Implications for the Foundations of Mathematics](https://arxiv.org/abs/2204.05123) (2022)
- Stephen Wolfram, [Observer Theory](https://writings.stephenwolfram.com/2023/12/observer-theory/) (2023)
- Stephen Wolfram, [What Is Ruliology?](https://writings.stephenwolfram.com/2026/01/what-is-ruliology/) (2026)
- Stephen Wolfram, [P vs. NP and the Difficulty of Computation: A Ruliological Approach](https://writings.stephenwolfram.com/2026/01/p-vs-np-and-the-difficulty-of-computation-a-ruliological-approach/) (2026)
- Stephen Wolfram, [What Ultimately Is There? Metaphysics and the Ruliad](https://writings.stephenwolfram.com/2026/02/what-ultimately-is-there-metaphysics-and-the-ruliad/) (2026)

### Technical Development

- Jonathan Gorard, [Some Relativistic and Gravitational Properties of the Wolfram Model](https://arxiv.org/abs/2004.14810) (2020)
- Jonathan Gorard, [Some Quantum Mechanical Properties of the Wolfram Model](https://doi.org/10.25088/ComplexSystems.29.2.537) (2020)
- Jonathan Gorard, [Algorithmic Causal Sets and the Wolfram Model](https://arxiv.org/abs/2011.12174) (2020)
- Xerxes D. Arsiwalla, Jonathan Gorard, and Hatem Elshatlawy, [Homotopies in Multiway Rewriting Systems as n-Fold Categories](https://arxiv.org/abs/2105.10822) (2022 journal version)
- Xerxes D. Arsiwalla and Jonathan Gorard, [Pregeometric Spaces from Wolfram Model Rewriting Systems as Homotopy Types](https://link.springer.com/article/10.1007/s10773-024-05576-0) (2024 journal version)
- Dean Rickles, Hatem Elshatlawy, and Xerxes D. Arsiwalla, [Ruliology: Linking Computation, Observers and Physical Law](https://arxiv.org/abs/2308.16068) (2023)
- Hatem Elshatlawy, Dean Rickles, Xerxes D. Arsiwalla, and Alexander Blum, [Towards a Generalized Theory of Observers](https://arxiv.org/abs/2504.16225) (2025)

### Context and Comparison

- Sumati Surya, [The Causal Set Approach to Quantum Gravity](https://link.springer.com/article/10.1007/s41114-019-0023-1) (2019)
- Jürgen Schmidhuber, [Algorithmic Theories of Everything](https://arxiv.org/abs/quant-ph/0011122) (2000)
- Max Tegmark, [The Mathematical Universe](https://arxiv.org/abs/0704.0646) (2007)
- Stanford Encyclopedia of Philosophy, [The Church–Turing Thesis](https://plato.stanford.edu/entries/church-turing/)
- Stanford Encyclopedia of Philosophy, [Structuralism in the Philosophy of Mathematics](https://plato.stanford.edu/entries/structuralism-mathematics/)
- Ilias Amrani, [Grothendieck's Homotopy Hypothesis](https://arxiv.org/abs/1112.1251) (2011)

### Criticism and Historical Caution

- Adam Becker, [Physicists Criticize Stephen Wolfram's Theory of Everything](https://www.scientificamerican.com/article/physicists-criticize-stephen-wolframs-theory-of-everything/) (2020).
- Scott Aaronson, [Book Review: A New Kind of Science](https://arxiv.org/abs/quant-ph/0206089) (2002). This addresses Wolfram's earlier physics proposals, not the 2021 Ruliad directly, but it remains relevant to claims about computational complexity, Bell correlations, and the need to distinguish simulation from physical derivation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
