// True once the stage has rescaled to a narrowed viewport. Chromium delivers the resize event
// after `set_viewport_size` returns, so `check_pack_panel` waits on this before measuring
// overflow. A function rather than an expression string: Playwright compiles an expression
// predicate inside the page, which the published policy refuses without `'unsafe-eval'`.
() => document.querySelector("#stage-wrap").getBoundingClientRect().width <= window.innerWidth;
