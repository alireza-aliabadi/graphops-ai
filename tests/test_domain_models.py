import pytest

from models.domain_models import (
    Chunk,
    Entity,
    Relationship,
    Source,
    SourceType,
)


def test_source_normalizes_required_text_and_has_stable_id() -> None:
    first = Source(" docs/a.md ", SourceType.MARKDOWN, "abc")
    second = Source("docs/a.md", SourceType.MARKDOWN, "abc")

    assert first.uri == "docs/a.md"
    assert first.id == second.id


def test_chunk_keeps_document_provenance() -> None:
    chunk = Chunk("document_1", "Graph retrieval", 0, 0, 15)

    assert chunk.document_id == "document_1"
    assert chunk.id.startswith("chunk_")


def test_entity_rejects_invalid_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        Entity("GraphRAG", "technology", "document_1", 1.1)


def test_relationship_keeps_evidence_and_rejects_self_reference() -> None:
    with pytest.raises(ValueError, match="itself"):
        Relationship("entity_1", "entity_1", "uses", 0.9, "chunk_1")

    relationship = Relationship(
        "entity_1",
        "entity_2",
        "uses",
        0.9,
        "chunk_1",
    )
    assert relationship.evidence_chunk_id == "chunk_1"
