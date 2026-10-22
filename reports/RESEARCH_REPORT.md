# Research report: AI procurement and commercial decision support

## Executive finding

The lowest quotation need not be the strongest risk-adjusted option. The default synthetic model shortlists Demo A (score 98.700), followed by Demo C (97.052) and Demo B (86.144). When cost receives only 20% of the score, Demo C wins all four modeled price scenarios. This is a sensitivity result from hypothetical costs and risks, not a real supplier award recommendation or negotiated saving.

## Research question and scope

How can an assistant help buyers compare offers, challenge assumptions and explain a commercial decision without automating authority? Three fictional quotations have a common EUR scope for one item. The assistant calculates costs and scores, produces a cited offline draft, and optionally asks an installed local Ollama model to write a recommendation from the calculated facts. No purchase, negotiation or supplier communication is executed. Optional live inference was not validated; adapter behavior was tested with mocked responses.

## Cost and score model

Landed cost is unit price × (1 + price shock) × (1 + duty rate) + freight per unit. Risk-adjusted cost adds defect probability × failure cost and late-delivery probability × delay cost. Cost utility is the minimum risk-adjusted cost divided by the supplier's risk-adjusted cost. The weighted score is 100 × [cost weight × cost utility + quality weight × (1 − defect rate) + delivery weight × (1 − late rate)]. Weights must be nonnegative and sum to one. Mixed currencies are rejected rather than silently compared.

Base landed costs are EUR 45.84 for A, 41.40 for B and 50.00 for C. Risk-adjusted costs are EUR 48.84, 57.40 and 51.30. B's lower price is outweighed by assumed defect and delay exposure. This conclusion is conditional on risk estimates and penalties; changing those assumptions can change the answer. Quality and delivery influence both cost and score, which can deliberately emphasize reliability but can also double-count it. A thesis should test a pure total-cost baseline and justify any added preference weighting.

## Scenario and assortment findings

The sensitivity grid combines four uniform price shocks (−10%, 0%, +10%, +25%) and three cost weights (20%, 50%, 80%). Remaining weight is split 60:40 between quality and delivery. C wins the four low-cost-weight cells; A wins the other eight. Uniform shocks do not capture supplier-specific exposure or correlations, so the table is not a probability forecast.

Assortment contribution equals (selling price − unit cost × cost factor − fulfillment cost) × units × volume factor − fixed cost. At baseline, four fictional SKUs contribute EUR 5,300, −800, 2,100 and 2,000. SKU-2 merits investigation under the assumptions, but the model lacks customer complementarity and strategic assortment value; it does not justify immediate delisting. The dashboard allows demand and cost stress to expose these trade-offs.

## Human decision support

The offline recommendation cites the winning quote and describes assumptions needing clarification. A lowest comparable landed-cost reference is a discussion anchor, not a promised negotiation target. Generated text remains separate from authoritative calculation. Changing ranking inputs invalidates a previously generated draft. Human approval requires an explicit commercial-assumptions check and a rationale; the stored artifact includes the ranking, settings and current generated draft.

## Proposed thesis validation

Map the purchasing decision process and define comparable quote scope with practitioners. Gather permitted historical cases and independently reconstruct realized landed and disruption costs. Backtest scores on time-separated cases and compare a price-only baseline, expected-total-cost model and multicriteria model. Study recommendation usefulness, overlooked exceptions, active review effort and automation bias with counterbalanced scenarios. Assess whether model wording causes reviewers to over-trust uncertain estimates.

Pricing research should distinguish list price, commercial terms, volume tiers and negotiated outcomes. Any claimed benefit should use realized outcomes with a suitable comparison and documented counterfactual assumptions. Assortment analysis should add working capital, substitutions and service obligations before operational use.

## Limitations

Synthetic rates are not calibrated probabilities. Expected-loss addition ignores correlations and tail severity. A shared price shock is simplistic. Self-declared reviewer identities and local audit storage are not production controls. No actual negotiation, enterprise validation or real commercial effect is claimed.

## Reproduction and evidence

Run `python -m portfolio.demo` from the repository root. Inputs are in `data/`; row-level or aggregate outputs are in `results/`. Run `python -m pytest -q` for the tested behavioral boundaries. All original synthetic materials are MIT-licensed.
