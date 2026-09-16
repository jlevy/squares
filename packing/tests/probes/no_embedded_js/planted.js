// The JavaScript `test_no_embedded_js_contract.py` plants in temporary Python modules to prove
// the guard refuses it. It lives here because a test that wrote it as a Python string would
// be the violation it is testing for.
() => location.href;
