// Apply any calls given and then seek to the last instant of whatever is on the stage, in
// one turn, because the duration has to be read after the calls have taken effect.
// o.calls is a list of [method, ...arguments], and may be empty.
(o) => {
  const api = window.atlasTransitions;
  for (const call of o.calls || []) {
    api[call[0]](...call.slice(1));
  }
  return api.seek(api.duration());
};
