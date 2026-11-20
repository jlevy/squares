# square-packing-211

Packing of 211 unit squares inside a square of side 14.9979607

This 211-square packing combines a 64-square rectangular component from Arslanov, Mustafin and Shangitbayev (2021), a computationally found 30-square component, and two aligned grids containing 99 and 18 squares. The numerical search and refinement were performed with GPT-6 Astra under the direction of Joost de Winter. Earlier solutions and optimization scripts supplied to the model had been developed with Claude Opus and previous GPT models.

## Sources

- M. Z. Arslanov, S. A. Mustafin and Z. K. Shangitbayev (2021). Improved packings of n(n − 1) unit squares in a square. The Electronic Journal of Combinatorics 28(4), P4.22. https://doi.org/10.37236/8586. Source of the construction with tilted components combined with grids, and of the 64-square rectangular component.
- Erich Friedman's collection of square packings (Packing Center, "Squares in Squares") and his survey: E. Friedman (2009). Packing unit squares in squares: A survey and new results. The Electronic Journal of Combinatorics, Dynamic Survey DS7. https://doi.org/10.37236/28. Source of the known packings used as starting points and for comparison.
- David Ellsworth's records of square packings, used as starting points and for comparison.

## Files

- `n211__record.json`: coordinates of the packing.
- `n211__record.svg`: figure of the packing.
