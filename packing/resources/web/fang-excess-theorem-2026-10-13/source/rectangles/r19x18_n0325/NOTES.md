325 unit squares in the box [0, W] x [0, H] with W = 18.994048655031..., H = 17.994048655031..., i.e. strictly inside the integer box 19 x 18 shrunk by d in both directions.

- box: 19 x 18
- count: 325
- waste in the box: 19 * 18 - 325 = 17 (= b - 1 with b = 18)
- squeeze d = min(19 - W, 18 - H) = 0.0059513 (rounded down)
- d exactly: 1012568876048606010046771487081655957/170141183460469231731687303715884105728
- seed: grown from the Kingbird n = 307 packing (Ellsworth, Stead) by one vertical cut through the lower wedge, then squeezed; found 2026-10-10; not analytically optimised.
