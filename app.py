TITLE='AI Procurement & Commercial Decision Support'

import json
from pathlib import Path
import streamlit as st
import pandas as pd
from portfolio.governance import ReviewStore, digest
ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title=TITLE,layout='wide')
st.title(TITLE)
st.warning('Synthetic portfolio demonstration. No real company data or validated business outcomes. Independent project; no company affiliation.')
def load(name): return json.loads((ROOT/'data'/name).read_text())
def review(artifact,blocked=False):
    st.subheader('Human review')
    st.caption('Self-declared demo reviewer. A decision applies only to this exact artifact version. Local SQLite audit; not enterprise authentication.')
    with st.form('review'):
        reviewer=st.text_input('Reviewer alias',value='demo-reviewer')
        decision=st.selectbox('Decision',['revise','approve','reject'])
        reason=st.text_area('Reason')
        submit=st.form_submit_button('Record human decision')
    store=ReviewStore(ROOT/'runtime'/'audit.sqlite')
    if submit:
        try:store.decide(digest(artifact),decision,reviewer,reason,blocked);st.success('Decision recorded')
        except ValueError as exc:st.error(str(exc))
    st.caption('Audit hash chain valid: '+str(store.verify()))
    st.dataframe(store.rows())
    st.download_button('Download audit JSON',json.dumps(store.rows(),indent=2),'audit.json')
    store.db.close()

from portfolio.procurement import rank_quotes, sensitivity, assortment, recommend, generate_recommendation
quotes=load('quotes.json');products=load('products.json')
cost_weight=st.slider('Cost weight',0.0,1.0,.5,.05)
shock=st.slider('Price shock',-.5,.5,0.0,.05)
weights={'cost':cost_weight,'quality':(1-cost_weight)*.6,'delivery':(1-cost_weight)*.4}
ranked=rank_quotes(quotes,weights,shock)
st.subheader('Quotation comparison and supplier scoring');st.dataframe(ranked)
st.bar_chart(pd.DataFrame(ranked).set_index('supplier')[['landed_cost','risk_adjusted_cost']])
st.info(recommend(ranked))
local_model=st.checkbox('Use optional local Ollama recommendation',False)
if st.button('Generate recommendation'):
    try:st.session_state['recommendation']={'fingerprint':digest(ranked),'text':generate_recommendation(ranked,local_model)}
    except Exception as exc:st.error('Generation failed: '+type(exc).__name__)
draft=st.session_state.get('recommendation',{})
current_draft=draft.get('text','') if draft.get('fingerprint')==digest(ranked) else ''
if current_draft:st.write(current_draft)
else:st.caption('Regenerate optional draft after changing ranking assumptions.')
st.subheader('Sensitivity grid');st.dataframe(sensitivity(quotes))
volume=st.slider('Assortment demand multiplier',0.0,2.0,1.0,.1)
profits=assortment(products,volume,1+shock);st.dataframe(profits)
st.bar_chart(pd.DataFrame(profits).set_index('sku')['contribution_eur'])
checked=st.checkbox('I verified comparable scope, currency and risk assumptions')
review({'ranking':ranked,'weights':weights,'shock':shock,'assumptions_checked':checked,'generated_draft':current_draft},not checked)
