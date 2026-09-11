// Drive the page's own API in one turn, so no frame can fall between the calls.
// o.calls is a list of [method, ...arguments]; the last call's answer comes back.
(o) => {
  const api = window.atlasTransitions;
  let answer;
  for (const call of o.calls) answer = api[call[0]](...call.slice(1));
  return answer;
}
