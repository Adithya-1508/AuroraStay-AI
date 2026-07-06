# Semantic Retrieval Manual

The `Retriever` processes incoming query strings, queries the Qdrant vector index, filters matching metadata payloads, and normalizes scores.

## Key APIs

- `Retriever.retrieve(query, collection_name, filter_meta, top_k)`: Executes semantic searches.
- `Retriever.register_query_expansion_hook(hook)`: Registers query rewrite functions.
