"""HTTP entry points for the GraphOps AI platform."""

from fastapi import FastAPI

from graphops_ai import __version__

app = FastAPI(
    title="GraphOps AI",
    description="Knowledge and inference platform for GraphRAG workloads.",
    version=__version__,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Return the liveness status of the API process."""

    return {"status": "ok", "version": __version__}
