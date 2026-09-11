// Write a mark on one identity's element, so a later read says whether it survived.
// Takes {identity, mark}.
(o) => { document.querySelector('#squares g[data-identity="' + o.identity + '"]').dataset.probe = o.mark; }
