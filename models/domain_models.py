"""Framework-independent domain models for GraphOps AI."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from json import dumps
from typing import Any

from validators.required import (
    confidence,
    non_empty,
    positive,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


def stable_id(namespace: str, values: Mapping[str, object]) -> str:
    payload = dumps(
        {"namespace": namespace, "values": values},
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return f"{namespace}_{sha256(payload.encode()).hexdigest()[:24]}"


class SourceType(StrEnum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    TEXT = "text"
    JSON = "json"
    GIT = "git"
    URL = "url"


class AgentStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class WorkloadStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Source:
    uri: str
    source_type: SourceType
    checksum: str
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "uri", non_empty(self.uri, "uri"))
        object.__setattr__(
            self,
            "checksum",
            non_empty(self.checksum, "checksum"),
        )

    @property
    def id(self) -> str:
        return stable_id(
            "source",
            {
                "uri": self.uri,
                "source_type": self.source_type.value,
                "checksum": self.checksum,
            },
        )


@dataclass(frozen=True, slots=True)
class Document:
    source_id: str
    title: str
    content: str
    metadata: Mapping[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_id",
            non_empty(self.source_id, "source_id"),
        )
        object.__setattr__(self, "title", non_empty(self.title, "title"))
        object.__setattr__(
            self,
            "content",
            non_empty(self.content, "content"),
        )

    @property
    def id(self) -> str:
        return stable_id(
            "document",
            {
                "source_id": self.source_id,
                "title": self.title,
                "content": self.content,
            },
        )


@dataclass(frozen=True, slots=True)
class Chunk:
    document_id: str
    content: str
    position: int
    start_offset: int
    end_offset: int
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "document_id",
            non_empty(self.document_id, "document_id"),
        )
        object.__setattr__(
            self,
            "content",
            non_empty(self.content, "content"),
        )
        if self.position < 0:
            raise ValueError("position must not be negative")
        if self.start_offset < 0:
            raise ValueError("start_offset must not be negative")
        if self.end_offset <= self.start_offset:
            raise ValueError("end_offset must be greater than start_offset")

    @property
    def id(self) -> str:
        return stable_id(
            "chunk",
            {
                "document_id": self.document_id,
                "content": self.content,
                "position": self.position,
                "start_offset": self.start_offset,
                "end_offset": self.end_offset,
            },
        )


@dataclass(frozen=True, slots=True)
class Entity:
    name: str
    entity_type: str
    source_document_id: str
    confidence: float
    source_chunk_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", non_empty(self.name, "name"))
        object.__setattr__(
            self,
            "entity_type",
            non_empty(self.entity_type, "entity_type"),
        )
        object.__setattr__(
            self,
            "source_document_id",
            non_empty(self.source_document_id, "source_document_id"),
        )
        if self.source_chunk_id is not None:
            object.__setattr__(
                self,
                "source_chunk_id",
                non_empty(self.source_chunk_id, "source_chunk_id"),
            )
        object.__setattr__(
            self,
            "confidence",
            confidence(self.confidence, "confidence"),
        )

    @property
    def id(self) -> str:
        return stable_id(
            "entity",
            {
                "name": self.name.casefold(),
                "entity_type": self.entity_type.casefold(),
                "source_document_id": self.source_document_id,
            },
        )


@dataclass(frozen=True, slots=True)
class Relationship:
    source_entity_id: str
    target_entity_id: str
    relation_type: str
    confidence: float
    evidence_chunk_id: str

    def __post_init__(self) -> None:
        for name in (
            "source_entity_id",
            "target_entity_id",
            "relation_type",
            "evidence_chunk_id",
        ):
            object.__setattr__(self, name, non_empty(getattr(self, name), name))
        if self.source_entity_id == self.target_entity_id:
            raise ValueError("relationship cannot connect an entity to itself")
        object.__setattr__(
            self,
            "confidence",
            confidence(self.confidence, "confidence"),
        )

    @property
    def id(self) -> str:
        return stable_id(
            "relationship",
            {
                "source_entity_id": self.source_entity_id,
                "target_entity_id": self.target_entity_id,
                "relation_type": self.relation_type,
                "evidence_chunk_id": self.evidence_chunk_id,
            },
        )


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    chunk_id: str
    content: str
    score: float
    retrieval_method: str
    document_id: str
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("chunk_id", "content", "retrieval_method", "document_id"):
            object.__setattr__(self, name, non_empty(getattr(self, name), name))
        if self.score < 0:
            raise ValueError("score must not be negative")


@dataclass(frozen=True, slots=True)
class Agent:
    name: str
    description: str
    endpoint: str
    capabilities: tuple[str, ...]
    status: AgentStatus = AgentStatus.ACTIVE

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", non_empty(self.name, "name"))
        object.__setattr__(
            self,
            "description",
            non_empty(self.description, "description"),
        )
        object.__setattr__(
            self,
            "endpoint",
            non_empty(self.endpoint, "endpoint"),
        )
        if not self.capabilities:
            raise ValueError("capabilities must not be empty")
        object.__setattr__(
            self,
            "capabilities",
            tuple(non_empty(item, "capability") for item in self.capabilities),
        )

    @property
    def id(self) -> str:
        return stable_id(
            "agent",
            {"name": self.name, "endpoint": self.endpoint},
        )


@dataclass(frozen=True, slots=True)
class AgentTask:
    agent_id: str
    task_type: str
    input: Mapping[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    id: str = field(default_factory=lambda: stable_id("task", {}))
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        object.__setattr__(self, "agent_id", non_empty(self.agent_id, "agent_id"))
        object.__setattr__(
            self,
            "task_type",
            non_empty(self.task_type, "task_type"),
        )
        object.__setattr__(self, "id", non_empty(self.id, "id"))


@dataclass(frozen=True, slots=True)
class InferenceRequest:
    model: str
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.0
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "model", non_empty(self.model, "model"))
        object.__setattr__(self, "prompt", non_empty(self.prompt, "prompt"))
        positive(self.max_tokens, "max_tokens")
        if not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be between 0.0 and 2.0")


@dataclass(frozen=True, slots=True)
class InferenceResponse:
    request_id: str
    model: str
    text: str
    input_tokens: int
    output_tokens: int
    latency_ms: float

    def __post_init__(self) -> None:
        for name in ("request_id", "model", "text"):
            object.__setattr__(self, name, non_empty(getattr(self, name), name))
        if self.input_tokens < 0 or self.output_tokens < 0:
            raise ValueError("token counts must not be negative")
        if self.latency_ms < 0:
            raise ValueError("latency_ms must not be negative")


@dataclass(frozen=True, slots=True)
class EvaluationSample:
    question: str
    reference_answer: str
    relevant_document_ids: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "question",
            non_empty(self.question, "question"),
        )
        object.__setattr__(
            self,
            "reference_answer",
            non_empty(self.reference_answer, "reference_answer"),
        )
        if not self.relevant_document_ids:
            raise ValueError("relevant_document_ids must not be empty")


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    sample_id: str
    retrieval_score: float
    answer_score: float
    latency_ms: float
    metrics: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "sample_id",
            non_empty(self.sample_id, "sample_id"),
        )
        object.__setattr__(
            self,
            "retrieval_score",
            confidence(self.retrieval_score, "retrieval_score"),
        )
        object.__setattr__(
            self,
            "answer_score",
            confidence(self.answer_score, "answer_score"),
        )
        if self.latency_ms < 0:
            raise ValueError("latency_ms must not be negative")


@dataclass(frozen=True, slots=True)
class GPUWorkload:
    request_id: str
    gpu_memory_mb: int
    priority: int = 0
    status: WorkloadStatus = WorkloadStatus.QUEUED
    gpu_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "request_id",
            non_empty(self.request_id, "request_id"),
        )
        positive(self.gpu_memory_mb, "gpu_memory_mb")
        if self.priority < 0:
            raise ValueError("priority must not be negative")
        if self.gpu_id is not None:
            object.__setattr__(
                self,
                "gpu_id",
                non_empty(self.gpu_id, "gpu_id"),
            )
