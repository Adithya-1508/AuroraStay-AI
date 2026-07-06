# Agent Platform: Checkpointing

This document describes checkpoint savers implementations.

## Savers Mappings

- **`BaseCheckpointer`**: Generic interface defining save, load, and list hooks.
- **`MemoryCheckpointer`**: Thread-safe in-memory checkpointer dictionary.
- **`PostgresCheckpointer`**: PostgreSQL database checkpointer table inserting, querying, and updating JSON state snapshots by session.
