401 unit squares in the box [0, W] x [0, H] with W = 20.988287236850..., H = 19.988287236850..., i.e. strictly inside the integer box 21 x 20 shrunk by d in both directions.

- box: 21 x 20
- count: 401
- waste in the box: 21 * 20 - 401 = 19 (= b - 1 with b = 20)
- squeeze d = min(21 - W, 20 - H) = 0.0117127 (rounded down)
- d exactly: 646708162215024128348295070074749798603034376056943621054663162610219/55213970774365330020306092093860176728400937535454490215772818314887168
- seed: grown from our n = 381 packing (n0381/) by one vertical cut through the lower wedge, then squeezed; found 2026-10-10; not analytically optimised.
