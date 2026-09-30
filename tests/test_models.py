from datetime import UTC, datetime

import pytest

from models.domain_models import (
    Chunk,
    Document,
    Entity,
    Relationship,
    Source,
    SourceType,
)


def test_source_id_is_stable() -> None:
    source1 = Source(
        uri="docs/architecture.md",
        source_type=SourceType.MARKDOWN,
        checksum="abc123",
    )
    source2 = Source(
        uri="docs/architecture.md",
        source_type=SourceType.MARKDOWN,
        checksum="abc123",
    )
    assert source1.id == source2.id


def test_document_id_changes_when_content_changes() -> None:
    created_at = datetime.now(UTC)

    document1 = Document(
        source_id="source_1",
        title="Architecture",
        content="original content",
        created_at=created_at,
    )
    document2 = Document(
        source_id="source_1",
        title="Architecture",
        content="updated content",
        created_at=created_at,
    )
    assert document1.id != document2.id


def test_chunk_preserves_document_provenance() -> None:
    chunk = Chunk(
        document_id="document_1",
        content="Graph retrieval uses entity neighborhoods.",
        position=0,
        start_offset=0,
        end_offset=50,
    )

    assert chunk.document_id == "document_1"
    assert chunk.id.startswith("chunk_")


def test_entity_rejects_invalid_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        Entity(
            name="GraphRAG",
            entity_type="technology",
            source_document_id="document_1",
            confidence=1.5,
        )


def test_relationship_rejects_self_reference() -> None:
    with pytest.raises(ValueError, match="itself"):
        Relationship(
            source_entity_id="entity_1",
            target_entity_id="entity_1",
            relation_type="depends_on",
            confidence=0.9,
            evidence_chunk_id="chunk_1",
        )


def test_relationship_preserves_evidence_provenance() -> None:
    relationship = Relationship(
        source_entity_id="entity_1",
        target_entity_id="entity_2",
        relation_type="uses",
        confidence=0.92,
        evidence_chunk_id="chunk_7",
    )

    assert relationship.evidence_chunk_id == "chunk_7"