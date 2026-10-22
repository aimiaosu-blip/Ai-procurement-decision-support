# Existing-repository review and reuse

The connected account was checked before development. None of the four requested repository names existed among the 11 accessible repositories. Existing repositories were not overwritten.

Reviewed README files:
- `aimiaosu-blip/automotive-supplier-claim-rag`: relevant TF-IDF, provenance and human-review design.
- `aimiaosu-blip/LLM-Assisted-Research-Review-Workflow-Prototype`: relevant human decision gate, explicit offline labels and hash-chain audit design.
- `aimiaosu-blip/Ai-service-sourcing-analytics-`: minimal README; not enough documented reusable interface to adopt safely.
- `aimiaosu-blip/omnichannel-commerce-growth-analytics-portfolio`: relevant synthetic-analysis and metric transparency approach; a consumer commerce domain, not this B2B research dataset.

New common components `governance.py` and `charts.py` are vendored identically across the four standalone projects. They are not claimed to be copied from the research-review project. This avoids a new externally hosted dependency while maintaining independent execution; future updates must synchronize these two files.

Project 4 actually reuses `automotive-supplier-claim-rag/src/claim_rag/text.py`, blob `b496b728e016b7041b1ad114d2cf03361881d4d6`, as `portfolio/reused_text.py`, under its MIT license. The cosine function is used by the retrieval path. Its tokenizer is intentionally not used because requirement IDs, single digits and units need different tokenization. Other projects reuse the new common components, not the supplier-claim domain data.
