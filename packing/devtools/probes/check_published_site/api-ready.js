// True once the deployed workbench has published its API, which `wait_for_function` polls for.
() => typeof window.atlasTransitions?.pairs === "function";
