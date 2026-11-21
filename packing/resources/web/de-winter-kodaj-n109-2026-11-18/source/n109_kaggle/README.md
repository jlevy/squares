# n = 109: public Kaggle coordinates (Tomáš Kodaj)

This folder holds a packing of 109 unit squares in a square of side 547464479047171949843/50000000000000000000 = 10.94928958094343899686, rounded up s(109) <= 10.949289580944. It supplies the coordinates for Squares Project issue #1012. The packing is not my work.

## Source

Tomáš Kodaj published the coordinates in his Kaggle dataset "Squares in Squares: strips and bands (coordinates)", version 2, 13 November 2026, under the licence CC0: Public Domain. His notebook "squares-in-squares-22-1636" copies the same submission.csv to its output. The SHA-256 of the full submission.csv is 7700b20d7c901a831741d0dbabae0941fefe460381cc18d969ec29aa728e489b.

- Dataset: https://www.kaggle.com/datasets/tomkodaj/squares-strips-and-bands/versions/2
- Notebook: https://www.kaggle.com/code/tomkodaj/squares-in-squares-22-1636

Kodaj asks readers to follow his source notebooks for the original credits. Navneet Prabhat's public compilation contains the same packing (side about 10.94928958094337). The 109-square pinwheel was published earlier by Guilherme Dias da Fonseca (6 November 2026, side 10.949392392), and Squares Project issue #958 documents a public pinwheel in Samanyu-dev's best_fit_101_500.csv at 10.94928958094538. Who made the last numerical refinement is unconfirmed.

## Files

- `n109_tomkodaj.csv`: the original header and the 109 rows for n = 109, with all digits, IDs and row order preserved (centres, angle in radians).
- `n109_tomkodaj.yaml`: an exact rational Witness/v2 transcription. Each orientation uses a rational tan(angle/2), so every square has exactly unit sides. The centres were translated into the first quadrant.
- `verification.txt`: output of the Squares Project's independent rational-corner checker (jlevy/squares at f9ddfeeef9070ede581142154ab992149b278ab0): 109 squares, 5,886 pairs, all interiors disjoint.

The transcription was made with GPT-6.2 Sol (OpenAI) and checked again with Claude (Anthropic), under the direction of Joost de Winter.
