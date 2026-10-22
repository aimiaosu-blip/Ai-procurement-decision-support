import math

def rank_quotes(quotes,weights=None,price_shock=0):
    weights=weights or {'cost':.5,'quality':.3,'delivery':.2}
    if set(weights)!={'cost','quality','delivery'} or any(not math.isfinite(v) or v<0 for v in weights.values()) or abs(sum(weights.values())-1)>1e-8: raise ValueError('Nonnegative weights must sum to one')
    if not math.isfinite(price_shock) or price_shock<=-1: raise ValueError('Invalid price shock')
    if not quotes:return []
    output=[]
    for q in quotes:
        for key in ['unit_price','freight_per_unit','duty_rate','defect_rate','late_rate','failure_cost','delay_cost']:
            if not math.isfinite(q[key]) or q[key]<0:raise ValueError('Invalid quote value')
        if q['currency']!='EUR':raise ValueError('Convert quotes to EUR before comparison')
        if q['defect_rate']>1 or q['late_rate']>1:raise ValueError('Rates must be within [0,1]')
        landed=q['unit_price']*(1+price_shock)*(1+q['duty_rate'])+q['freight_per_unit']
        risk=landed+q['defect_rate']*q['failure_cost']+q['late_rate']*q['delay_cost']
        if risk<=0:raise ValueError('Positive total cost required')
        output.append(dict(q,landed_cost=round(landed,4),risk_adjusted_cost=round(risk,4)))
    minimum=min(r['risk_adjusted_cost'] for r in output)
    for r in output:
        r['score']=round(100*(weights['cost']*minimum/r['risk_adjusted_cost']+weights['quality']*(1-r['defect_rate'])+weights['delivery']*(1-r['late_rate'])),3)
    return sorted(output,key=lambda r:(-r['score'],r['supplier']))

def sensitivity(quotes):
    result=[]
    for shock in [-.1,0,.1,.25]:
        for cost_weight in [.2,.5,.8]:
            weights={'cost':cost_weight,'quality':(1-cost_weight)*.6,'delivery':(1-cost_weight)*.4}
            ranked=rank_quotes(quotes,weights,shock)
            result.append(dict(price_shock=shock,cost_weight=cost_weight,winner=ranked[0]['supplier'],score=ranked[0]['score'],risk_adjusted_cost=ranked[0]['risk_adjusted_cost']))
    return result

def assortment(products,volume_factor=1,cost_factor=1):
    if volume_factor<0 or cost_factor<0:raise ValueError('Factors cannot be negative')
    return [dict(p,contribution_eur=round((p['sell_price']-p['unit_cost']*cost_factor-p['fulfilment_cost'])*p['units']*volume_factor-p['fixed_cost'],2)) for p in products]

def recommend(ranked):
    if not ranked:return 'Insufficient evidence: no comparable quotations.'
    best=ranked[0]
    return (f"Offline rule-based decision draft (not LLM inference): shortlist {best['supplier']} with score {best['score']:.3f}/100 and risk-adjusted unit cost EUR {best['risk_adjusted_cost']:.2f}. "
            f"Source: quote {best['quote_id']}. Request clarification of defect and delivery assumptions; use the lowest comparable landed cost EUR {min(r['landed_cost'] for r in ranked):.2f} as a discussion reference, not a guaranteed negotiation target. Human approval required.")


def generate_recommendation(ranked, use_local_model=False):
    """Optional local generation; calculated ranking remains authoritative."""
    baseline=recommend(ranked)
    if not use_local_model or not ranked: return baseline
    import os, json, urllib.request
    model=os.environ.get('OLLAMA_MODEL')
    if not model: raise ValueError('Set OLLAMA_MODEL to an installed local model')
    prompt='Draft a short procurement recommendation from only these calculated facts. Cite quote IDs. Do not change the ranking or claim approval. State uncertainty. '+json.dumps(ranked)
    body=json.dumps({'model':model,'prompt':prompt,'stream':False}).encode()
    request=urllib.request.Request('http://127.0.0.1:11434/api/generate',data=body,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=60) as response: output=json.load(response)['response']
    if not isinstance(output,str) or not output.strip(): raise ValueError('Empty model response')
    return 'LOCAL LLM DRAFT — factual support and citations require human verification.\n'+output
