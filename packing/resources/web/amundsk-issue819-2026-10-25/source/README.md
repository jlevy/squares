# s(344) ≤ 18.992567544845

A packing of 344 unit squares in a square of side 18.992567544845 (Amund Kristiansen, 2026-10-25). Dedicated to the public domain under CC0 1.0.

| file | contents | SHA-256 |
|---|---|---|
| `s344_amund.cert` | exact rational dilation certificate (δ = 1e-12); side S′ = 9496283772422138783772412642309/500000000000000000000000000000 | `4e2c6880812a688a64c8f378f5feb27a8a1a362f0d9161c0cda201f444526e21` |
| `s344_amund.input.txt` | the float64 packing it was made from (`n side`, then `x y angle_deg`) | `32cd4883edde91d300ef6b8f8cffc77972d2ad8ca1038101756f1ce8d2d233e5` |

Made with Evan Daniel's `search/packer/dilate_cert.py` at evand/square-packing `7982d7a9346e29e36cab3ce075274f3023114353` (macOS arm64, Python 3.14.6); check with that commit's `search/exact/verify_cert.py` and `verify_cert2.py`.
