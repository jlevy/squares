257 unit squares in the box [0, W] x [0, H] with W = 16.999256308446..., H = 15.999256308446..., i.e. strictly inside the integer box 17 x 16 shrunk by d in both directions.

- box: 17 x 16
- count: 257
- waste in the box: 17 * 16 - 257 = 15 (= b - 1 with b = 16)
- squeeze d = min(17 - W, 16 - H) = 0.0007436 (rounded down)
- d exactly: 126532561084761488992828749143827311/170141183460469231731687303715884105728
- seed: grown from the Kingbird n = 241 packing (Ellsworth, Stead) by one vertical cut through the lower wedge, then squeezed; found 2026-10-09; not analytically optimised.
