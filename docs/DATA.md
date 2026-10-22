# Data contract and metrics

`quotes.json`: three fictional offers for one comparable item, all in EUR. Unit price, freight, failure cost and delay cost are currency per unit; duty, defect and late rates are fractions (0.02 means 2%). The shared failure penalty is 100 and delay penalty 40. All rows are synthetic. This is not an employer quotation dataset.

`products.json`: four fictional SKU records with EUR selling price, unit cost, fulfillment cost, fixed cost and assumed unit demand. Contribution is not net profit and does not include tax or working capital. Parameters are explicitly listed in the research report and source code.

Supplier scoring normalizes cost against the lowest risk-adjusted cost in the current scenario. Scores are preference utilities, not probabilities. The 12 sensitivity scenarios are an illustrative grid, not forecast quantiles.
