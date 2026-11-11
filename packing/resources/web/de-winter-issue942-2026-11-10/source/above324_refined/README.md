# Refined public packings above n = 324

Sixteen packings of n unit squares in a square. Each has a smaller side than the best value in the Squares Project register (repository `jlevy/squares` at commit f54ad104, 9 November 2026) and than the best public packing of the Kaggle competition "Squares in Squares" that I could find.

| n | New side, rounded up | Best public competition value | Register value | Gain over best public |
| ---: | ---: | ---: | ---: | ---: |
| 632 | 25.6456954277 | 25.6460731755 | 25.6568542495 | 3.8e-04 |
| 637 | 25.7447388658 | 25.7447480924 | 25.7692895103 | 9.2e-06 |
| 655 | 25.9996711101 | 25.9997111248 | 26.0000000000 | 4.0e-05 |
| 684 | 26.6456964776 | 26.6460731833 | 26.6568542495 | 3.8e-04 |
| 685 | 26.6870020013 | 26.6870514965 | 26.6923881597 | 4.9e-05 |
| 744 | 27.7601633593 | 27.7601696095 | 27.7867158070 | 6.3e-06 |
| 750 | 27.8595204745 | 27.8595284738 | 27.8745855412 | 8.0e-06 |
| 756 | 27.9245802503 | 27.9245818149 | 27.9496026382 | 1.6e-06 |
| 805 | 28.8450303356 | 28.8450375703 | 28.8582163416 | 7.2e-06 |
| 814 | 28.9549571055 | 28.9549585758 | 28.9614408088 | 1.5e-06 |
| 918 | 30.7867372035 | 30.7867520399 | 30.7960576884 | 1.5e-05 |
| 921 | 30.8271449853 | 30.8271453670 | 30.8396216603 | 3.8e-07 |
| 924 | 30.8553857463 | 30.8553859309 | 30.8708286934 | 1.8e-07 |
| 935 | 30.9800571865 | 30.9800574656 | 30.9941740581 | 2.8e-07 |
| 970 | 31.6389903231 | 31.6391025154 | 31.6568542495 | 1.1e-04 |
| 989 | 31.8889473785 | 31.8890306338 | 31.9096793514 | 8.3e-05 |

## Construction

The starting packings come from the file `data_out/best_certified_22.2226173_before_clearance.csv` in the repository `Samanyu-dev/squares_in_squares` at commit 53551d7. That file is a per-puzzle merge of public Kaggle notebooks and datasets. Its README credits Chris Deotte, lightningv08, alexchilton, kirilltym, malyshevdanil, prvsiyan, busyaprime, nilanjansaha123, jazivxt and the register of Francisco Couzo. The file does not name the author of each packing.

All 1000 packings of that file were tested for a remaining descent direction with a linear program on the contact constraints. Sixteen packings still had one. Following the descent to convergence gave the values in the table. The arrangements of the squares are unchanged.

Each certificate carries a margin of about 5e-9 above the numerical optimum.

## Files

- `nNNNN.cert`: exact rational certificate. First data line: n and the side. Then one line per square: centre x, centre y, and t = tan(theta/2) for the rotation angle theta.
- `verify_cert.py`: exact checker (containment and pairwise disjoint interiors, rational arithmetic). Run `python3 -B verify_cert.py` (Python 3.10 or later, standard library only).
- `SHA256SUMS`: checksums.

## Method and AI assistance

The descent test, local optimization, rational certificates and checking were produced with Claude (Anthropic) under the direction of Joost de Winter.
