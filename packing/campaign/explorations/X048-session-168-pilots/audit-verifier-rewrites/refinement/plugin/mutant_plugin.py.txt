"""A pytest plugin that substitutes a mutant kernel verifier for the committed one.

Loaded with `-p mutant_plugin` (this file copied to `mutant_plugin.py` on the plugin
path) and the environment variable R6_MUTANT naming the mutant file. The mutant is
installed in `sys.modules` under the committed module's name before collection, so
`from devtools import verify_n17_kernel_certificate` in the tests binds the mutant. The
repository's own files are never touched.
"""

from __future__ import annotations

import importlib.util
import os
import sys

NAME = "devtools.verify_n17_kernel_certificate"


def _install() -> None:
    path = os.environ.get("R6_MUTANT")
    if not path:
        return
    import devtools  # noqa: F401 - the package must exist before its submodule is set

    spec = importlib.util.spec_from_file_location(NAME, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[NAME] = module
    spec.loader.exec_module(module)
    setattr(sys.modules["devtools"], "verify_n17_kernel_certificate", module)


_install()
