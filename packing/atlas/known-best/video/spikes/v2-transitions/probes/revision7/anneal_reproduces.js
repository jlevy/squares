// One level's trajectory, then another level's, then the first level's again: the two
// readings say whether a level reproduces itself rather than caching something else.
// Takes {index}; leaves the dial back at its default.
(o) => {
  const A = window.atlasTransitions;
  A.setAnneal(7);
  const a = A.physics(o.index, 'bodies', 'free').final[0];
  A.setAnneal(2); A.physics(o.index, 'bodies', 'free');
  A.setAnneal(7);
  const b = A.physics(o.index, 'bodies', 'free').final[0];
  A.setAnneal(3);
  return [a, b];
}
