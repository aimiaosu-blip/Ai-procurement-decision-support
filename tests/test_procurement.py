import json, unittest
from portfolio.procurement import *
class ProcurementTests(unittest.TestCase):
    def setUp(self): self.quotes=json.loads(__import__('pathlib').Path('data/quotes.json').read_text())
    def test_cost_hand_calculation(self):
        row=next(r for r in rank_quotes(self.quotes) if r['supplier']=='Demo A')
        self.assertAlmostEqual(row['landed_cost'],45.84)
        self.assertAlmostEqual(row['risk_adjusted_cost'],48.84)
    def test_weights_currency(self):
        with self.assertRaises(ValueError): rank_quotes(self.quotes,{'cost':1,'quality':1,'delivery':1})
        with self.assertRaises(ValueError): rank_quotes([dict(self.quotes[0],currency='USD')])
    def test_shock_monotonic_cost(self):
        base={r['supplier']:r for r in rank_quotes(self.quotes)}
        self.assertTrue(all(r['risk_adjusted_cost']>base[r['supplier']]['risk_adjusted_cost'] for r in rank_quotes(self.quotes,price_shock=.1)))
    def test_profit_and_empty(self):
        p=dict(sku='X',sell_price=10,unit_cost=5,fulfilment_cost=1,units=10,fixed_cost=50)
        self.assertEqual(assortment([p])[0]['contribution_eur'],-10)
        self.assertIn('Insufficient',recommend([]))
    def test_sensitivity_grid(self): self.assertEqual(len(sensitivity(self.quotes)),12)

    def test_local_recommendation_mocked(self):
        from unittest.mock import patch, MagicMock
        response=MagicMock();response.__enter__.return_value.read.return_value=b'{"response":"Inspect Q1 before approval"}'
        with patch.dict('os.environ',{'OLLAMA_MODEL':'test'}),patch('urllib.request.urlopen',return_value=response):
            self.assertIn('LOCAL LLM DRAFT',generate_recommendation(rank_quotes(self.quotes),True))
