// Stop `check_math_loading/first_paint`'s frame sampler, where it is installed.
() => {
  if (globalThis.__mathLoadingState) {
    globalThis.__mathLoadingState.stop = true;
  }
};
