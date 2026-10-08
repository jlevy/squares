"""Pure scheduling, receipt, and axiom checks used by the serial verifier."""
import hashlib
import heapq
import json
import re


STANDARD_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
PUBLIC_TARGETS = {'ElevenSquare.Pending.' + name for name in (
    'baseline_certificate_exists', 'prior_certificate_exists',
    'returned_certificate_exists', 'global_lower_bound')} | {
    'ElevenSquare.optimality', 'ElevenSquare.optimal_side_lower_bound'}
_GLOBAL_TARGETS = {'ElevenSquare.Pending.global_lower_bound',
                   'ElevenSquare.optimality', 'ElevenSquare.optimal_side_lower_bound'}
_ADMISSION_TARGETS = {
    'ElevenSquare/Tasks/T01/Handoff/LeafCalculations.lean':
        'ElevenSquare.Pending.baseline_certificate_exists',
    'ElevenSquare/Tasks/T01/Handoff/PlanData.lean':
        'ElevenSquare.Pending.baseline_certificate_exists',
    'ElevenSquare/Tasks/T01/Handoff/ProgramCalculations.lean':
        'ElevenSquare.Pending.baseline_certificate_exists',
    'ElevenSquare/Pending/S06_PriorSupport.lean':
        'ElevenSquare.Pending.prior_certificate_exists',
    'ElevenSquare/Pending/S06_Returned.lean':
        'ElevenSquare.Pending.returned_certificate_exists',
    'ElevenSquare/Tasks/T07/UnfinishedCapture.lean': None,
}
# Additional component queries in ProofAudit. Keep these tied to their exact
# inventoried site: a remaining returned admission cannot excuse a capture
# admission (or vice versa), and neither permits sorryAx in completed families.
_ADMISSION_COMPONENT_TARGETS = {
    'ElevenSquare/Pending/S06_Returned.lean': {
        'ElevenSquare.Pending.returned_excluded'},
    'ElevenSquare/Tasks/T07/UnfinishedCapture.lean': {
        'ElevenSquare.Tasks.T07.case438_near_certificate'},
}


def admitted_targets(sites):
    """Allow inherited sorryAx only for the explicitly inventoried obligations."""
    paths = {site['path'] for site in sites}
    unknown = paths - _ADMISSION_TARGETS.keys()
    if unknown:
        raise ValueError('Unknown admission paths: ' + ', '.join(sorted(unknown)))
    targets = {_ADMISSION_TARGETS[path] for path in paths} - {None}
    for path in paths:
        targets.update(_ADMISSION_COMPONENT_TARGETS.get(path, set()))
    return targets | (_GLOBAL_TARGETS if paths else set())


def native_axiom_owner(name):
    """Recognize Lean 4.34's per-declaration native_decide axiom names only."""
    match = re.fullmatch(r'(.+)\._native\.native_decide\.ax_[0-9]+_[0-9]+', name)
    return match[1] if match else None


def native_trust_status(axioms, *, has_native_sources=False):
    """Report the trust actually inherited by audited declarations."""
    native = sorted({axiom for values in axioms.values() for axiom in values
                     if native_axiom_owner(axiom) is not None})
    return {'trust_model': ('lean_kernel_and_native_compiler'
                            if native or has_native_sources else 'lean_kernel'),
            'native_certificate_axioms': native}


def public_audit_status(axioms, admission_count):
    """Require every public query even after its permission for sorryAx closes."""
    missing = PUBLIC_TARGETS - axioms.keys()
    if missing:
        raise ValueError('Missing final public target axiom queries: ' + ', '.join(sorted(missing)))
    proved = admission_count == 0 and not any('sorryAx' in values for values in axioms.values())
    trust = native_trust_status(axioms)
    status = ('OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES'
              if trust['native_certificate_axioms'] else 'OPTIMALITY_PROVED')
    return {'status': status if proved else 'PARTIAL_ASSEMBLY_COMPILES',
            'global_optimality_proved': proved, **trust}


def priority_order(dependencies, sizes, final='ElevenSquare.Verification'):
    """Check shared interfaces before independent certificate leaves, serially."""
    users = {m: set() for m in dependencies}
    remaining = {m: len(set(ds)) for m, ds in dependencies.items()}
    for m, ds in dependencies.items():
        for dep in ds:
            users[dep].add(m)
    if users.get(final):
        raise ValueError('The final audit module must not have local dependents')
    key = lambda m: (m == final, -len(users[m]), sizes[m], m)
    ready = [key(m) for m, n in remaining.items() if n == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        m = heapq.heappop(ready)[-1]
        order.append(m)
        for user in users[m]:
            remaining[user] -= 1
            if remaining[user] == 0:
                heapq.heappush(ready, key(user))
    if len(order) != len(dependencies):
        raise ValueError('Local import cycle')
    return order


def input_digest(inputs):
    return hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()


def positive_jobs(value):
    """Parse a canonical positive thread count supported by Lean's UInt32 CLI."""
    if not isinstance(value, str) or not re.fullmatch(r'[1-9][0-9]*', value):
        raise ValueError('jobs must be a positive decimal integer')
    jobs = int(value)
    if jobs >= 2**32:
        raise ValueError('jobs must be less than 2**32')
    return jobs


def lean_arguments(module, jobs=1):
    """The only accepted proof settings; worker count does not change them."""
    if type(jobs) is not int or not 0 < jobs < 2**32:
        raise ValueError('jobs must be a positive UInt32 integer')
    implicit = 'true' if module == 'Sqpack' or module.startswith('Sqpack.') else 'false'
    return [f'-j{jobs}', '-M0', '-s65536', '-DautoImplicit=' + implicit, '-DmaxHeartbeats=0']


def recorded_arguments(module, arguments):
    """Reconstruct canonical arguments, rejecting every other recorded flag."""
    if (not isinstance(arguments, list) or not arguments
            or not isinstance(arguments[0], str) or not arguments[0].startswith('-j')):
        raise ValueError('Noncanonical compiler arguments: ' + module)
    try:
        expected = lean_arguments(module, positive_jobs(arguments[0][2:]))
    except ValueError as error:
        raise ValueError('Noncanonical compiler arguments: ' + module) from error
    if arguments != expected:
        raise ValueError('Noncanonical compiler arguments: ' + module)
    return expected


def reusable_inputs(old, current, *, legacy_baseline, checked_at, newest_input):
    if old == current:
        return True
    # Old receipts recorded only direct object hashes. Migrate them only in the
    # original checkout: its logs, objects and all dependency checks must predate
    # the receipt. Future receipts use hashes, including transitive input hashes.
    legacy = {k: v for k, v in current.items()
              if k not in {'build_context', 'local_dependency_inputs'}}
    return (legacy_baseline and old == legacy and newest_input <= checked_at)


def reusable_fingerprint(module, old, current, *, legacy_baseline, checked_at, newest_input):
    """Reuse unchanged evidence with its actual worker count, never relabel it.

    Requested jobs apply only to a new compilation. Every other current input
    still has to match, including transitive dependency fingerprints. The legacy
    migration retains its existing provenance and timestamp requirements.
    """
    if not isinstance(old, dict):
        return None
    try:
        candidate = dict(current, arguments=recorded_arguments(module, old.get('arguments')))
    except ValueError:
        return None
    if reusable_inputs(old, candidate, legacy_baseline=legacy_baseline,
                       checked_at=checked_at, newest_input=newest_input):
        return candidate
    return None


def audit_axioms(source_code, output, allowed, unfinished, native_declarations=frozenset()):
    queries = re.findall(r'^\s*#print\s+axioms\s+(\S+)', source_code, re.M)
    printed = re.findall(
        r"^'([^']+)' (?:depends on axioms: \[([^]]*)\]|(does not depend on any axioms))",
        output, re.M)
    if len(queries) != len(printed):
        raise ValueError(f'Expected {len(queries)} axiom outputs, found {len(printed)}')
    seen = {}
    for query, (name, axioms, _) in zip(queries, printed):
        query = query.removeprefix('_root_.')
        if name != query and not name.endswith('.' + query):
            raise ValueError('Missing axiom output: ' + query)
        axioms = {a.strip() for a in axioms.split(',') if a.strip()}
        # Each native axiom must belong to an exact declaration recorded in the
        # reviewed source manifest. No wildcard namespace or generic native
        # oracle is accepted, and native computation never permits sorryAx.
        approved_native = {a for a in axioms if native_axiom_owner(a) in native_declarations}
        extra = axioms - allowed - approved_native - ({'sorryAx'} if name in unfinished else set())
        if extra:
            raise ValueError('Unapproved axioms in ' + name + ': ' + str(sorted(extra)))
        seen[name] = sorted(axioms)
    return seen
