# s(303) ≤ 17.909762327476

A packing of 303 unit squares in a square of side 17.909762327476 (Amund Kristiansen, 2026-10-23).

| file | contents | SHA-256 |
|---|---|---|
| `s303_amund.cert` | exact rational certificate (dilation certificate, δ = 1e-12); side S′ = 223872029093440709529093216833/12500000000000000000000000000 = 17.909762327475256427… | `9ec01059b35cc983cb28a1bb33bd215a2717228f7efd182e1724de6b22dc511b` |
| `s303_amund.input.txt` | the float64 packing it was made from: `n side`, then `x y angle_deg` per square (side 17.909762327457347) | `19fc5d171a26bf8d4a925c0457fa367b12127e8bd581d91c6dcd573108e4bba4` |

Certificate format and checkers: Evan Daniel's [evand/square-packing](https://github.com/evand/square-packing) at
commit `7982d7a9346e29e36cab3ce075274f3023114353` (`search/packer/dilate_cert.py` made it;
`search/exact/verify_cert.py` and `search/exact/verify_cert2.py` check it, exact rational, standard library only):

    python3 search/exact/verify_cert.py  s303_amund.cert
    python3 search/exact/verify_cert2.py s303_amund.cert
