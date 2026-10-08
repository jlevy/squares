() =>
  typeof Reflect.get(window, "packWorkbench")?.state === "function" &&
  typeof Reflect.get(window, "searchWorkbench")?.state === "function";
