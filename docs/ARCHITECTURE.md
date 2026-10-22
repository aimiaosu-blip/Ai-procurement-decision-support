# Architecture and trust boundary

Input files → domain analysis → inspectable results → dashboard → optional human disposition → local audit.

Domain functions have no network dependency. Display charts are calculated from the same result objects used for JSON exports. Input data remains local. Only Projects 1 and 3's explicitly selected Ollama modes makes a request, to loopback port 11434. No cloud endpoint or API key is required or embedded.

Policy or input changes produce a new artifact hash. Human disposition requires a reviewer alias and a nonempty reason. Unresolved exceptions or unchecked factual/commercial assumptions block approval. The local database uses a transaction and a single final decision per artifact. There is no SSO, access control, encrypted database, server-grade audit integrity or multi-tenant isolation. Do not deploy this as an enterprise service.
