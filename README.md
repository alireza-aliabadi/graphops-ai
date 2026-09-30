# GraphOps AI

GraphOps AI is a production-style GraphRAG platform that combines a knowledge
graph, vector retrieval, model serving, GPU-aware scheduling, evaluation, and
agent interoperability.

## Development

Requirements: Python 3.11 and [Poetry](https://python-poetry.org/).

```bash
poetry install
make check
make run
```

The API liveness endpoint is available at <http://localhost:8000/health>.
Interactive OpenAPI documentation is available at
<http://localhost:8000/docs>.

## Repository layout

- `src/graphops_ai/` — application code
- `tests/` — automated tests
- `docs/architecture.md` — current system boundary and planned components
- `GraphOps-AI-PROGRESS.md` — implementation roadmap

The project is being built incrementally for constrained local hardware. Model
providers and infrastructure integrations remain behind replaceable interfaces.