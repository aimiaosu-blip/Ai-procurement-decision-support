import json
from pathlib import Path
from portfolio.charts import bars
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
def load(name): return json.loads((ROOT/'data'/name).read_text())
def write(name,value): (OUT/name).write_text(json.dumps(value,indent=2)+'\n')

from portfolio.procurement import *
quotes=load('quotes.json');ranked=rank_quotes(quotes);profits=assortment(load('products.json'))
write('metrics.json',{'ranking':ranked,'sensitivity':sensitivity(quotes),'assortment':profits,'recommendation':recommend(ranked)})
bars({r['supplier']:r['score'] for r in ranked},OUT/'overview.svg','Synthetic supplier weighted score / 100')

print('Rebuilt synthetic outputs in',OUT)
