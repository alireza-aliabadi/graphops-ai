# GraphOps AI — PROGRESS.md

> **Flagship AI Engineer portfolio project:** a production-style GraphRAG + Knowledge Graph + Hugging Face + vLLM + GPU Scheduling + Evaluation + A2A multi-agent platform.
>
> **Primary goal:** demonstrate end-to-end AI Software Engineering ability rather than building another basic RAG chatbot.

---

## 0. Project Definition

### Project name

**GraphOps AI**

### One-line description

GraphOps AI is an AI engineering platform that ingests technical knowledge, builds a knowledge graph, combines graph retrieval with vector retrieval, serves Hugging Face models through vLLM, schedules inference workloads, evaluates retrieval/generation quality, and enables independent AI agents to collaborate through A2A.

### Target interview story

> "I designed and implemented an AI platform that separates knowledge representation, retrieval, agent orchestration, model serving, GPU scheduling, and evaluation. I developed it on constrained local hardware and made the inference layer portable to larger GPU infrastructure."

### Core capabilities

- Knowledge graph construction
- Entity and relationship extraction
- Vector retrieval
- Graph retrieval
- Hybrid GraphRAG
- Hugging Face Transformers
- vLLM model serving
- GPU-aware inference scheduling
- Multi-agent orchestration
- A2A agent interoperability
- Automated RAG evaluation
- LLM generation evaluation
- Latency/throughput benchmarking
- Observability
- Dockerized local deployment
- Kubernetes deployment manifests
- Technical documentation and architecture decision records

---

# 1. Hardware Constraints

Development machine:

```text
CPU: 4 cores
RAM: 8 GB
GPU: 4 GB VRAM
```

## Local-development principle

Do NOT design the project around large local models.

Use:

```text
small/quantized generation model
small embedding model
small reranker
small evaluation dataset
small document corpus
```

The architecture must remain model-provider agnostic so a remote GPU can later run larger models.

### Local profile

```text
                     Local machine
                         │
             ┌───────────┴───────────┐
             │                       │
        CPU services             GPU service
             │                       │
     API / graph / DB          small HF model
     evaluation / agents             │
                                     ▼
                                    vLLM
```

### Remote-GPU profile

```text
Application services
        │
        ▼
Model Router
        │
        ▼
GPU Scheduler
        │
        ├── GPU Node A → vLLM
        ├── GPU Node B → vLLM
        └── GPU Node C → vLLM
```

---

# 2. Engineering Principles

1. **No LangChain dependency in the core architecture.**
2. Keep retrieval, graph, inference, agents, and evaluation as independent modules.
3. Use interfaces/protocols so implementations can be replaced.
4. Every important AI component must have tests.
5. Every optimization must have a benchmark.
6. Never claim performance numbers without measured experiments.
7. Keep local hardware requirements realistic.
8. Prefer reproducible Docker/Makefile commands.
9. Keep model serving behind an OpenAI-compatible internal interface.
10. A2A is used for agent-to-agent communication; MCP can optionally be used for agent-to-tool/data access.
11. Store experiment results as versioned artifacts.
12. Document important architectural decisions in `docs/adr/`.

---

# 3. Target Architecture

```text
                                  ┌─────────────────────┐
                                  │      Web Client     │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │     API Gateway     │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │ A2A Agent Router     │
                                  └──────────┬──────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
             Research Agent            RCA Agent               Code Agent
                    │                        │                        │
                    └────────────────────────┼────────────────────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │    GraphRAG Engine  │
                                  └──────────┬──────────┘
                                             │
                           ┌─────────────────┴─────────────────┐
                           │                                   │
                           ▼                                   ▼
                    ┌──────────────┐                    ┌──────────────┐
                    │ Vector Index │                    │ Knowledge    │
                    │              │                    │ Graph        │
                    └──────┬───────┘                    └──────┬───────┘
                           │                                   │
                           └─────────────────┬─────────────────┘
                                             ▼
                                  ┌─────────────────────┐
                                  │ Context Builder     │
                                  │ + Reranker          │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │ Model Router        │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │ GPU Workload        │
                                  │ Scheduler           │
                                  └──────────┬──────────┘
                                             │
                                             ▼
                                  ┌─────────────────────┐
                                  │ vLLM                 │
                                  │ HF Transformer Model │
                                  └─────────────────────┘

        ┌──────────────────────────────────────────────────────────────┐
        │ Observability + Evaluation                                   │
        │ OpenTelemetry / Prometheus / Grafana / Evaluation Harness    │
        └──────────────────────────────────────────────────────────────┘
```

---

# 4. Repository Structure

Target repository:

```text
graphops-ai/
├── apps/
│   ├── api/
│   ├── ingestion/
│   ├── graph/
│   ├── retrieval/
│   ├── inference-router/
│   ├── scheduler/
│   └── agents/
│
├── packages/
│   ├── domain/
│   ├── config/
│   ├── observability/
│   └── evaluation/
│
├── agents/
│   ├── orchestrator/
│   ├── research/
│   ├── rca/
│   ├── code/
│   └── evaluator/
│
├── graphrag/
│   ├── ingestion/
│   ├── chunking/
│   ├── extraction/
│   ├── entities/
│   ├── relationships/
│   ├── graph_builder/
│   ├── graph_retriever/
│   ├── vector_retriever/
│   ├── hybrid_retriever/
│   └── context_builder/
│
├── models/
│   ├── embeddings/
│   ├── reranker/
│   └── generation/
│
├── inference/
│   ├── vllm/
│   ├── model_registry/
│   └── health/
│
├── scheduler/
│   ├── queue/
│   ├── policies/
│   ├── resources/
│   └── metrics/
│
├── a2a/
│   ├── agent_cards/
│   ├── client/
│   ├── server/
│   └── tasks/
│
├── evaluation/
│   ├── datasets/
│   ├── retrieval/
│   ├── generation/
│   ├── regression/
│   ├── benchmarks/
│   └── reports/
│
├── infrastructure/
│   ├── docker/
│   ├── compose/
│   ├── kubernetes/
│   ├── helm/
│   └── monitoring/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── evaluation/
│   └── load/
│
├── docs/
│   ├── architecture.md
│   ├── graphrag.md
│   ├── inference.md
│   ├── gpu-scheduling.md
│   ├── evaluation.md
│   ├── a2a.md
│   └── adr/
│
├── experiments/
│   ├── retrieval/
│   ├── inference/
│   └── scheduling/
│
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── README.md
└── PROJECT_PROGRESS.md
```

---

# 5. Phase 0 — Repository Bootstrap

## Objectives

- Create repository
- Establish Python project
- Configure linting/type checking
- Establish Docker development environment
- Establish CI

## Tasks

- [ ] Create Git repository
- [ ] Create `README.md`
- [ ] Create this `PROJECT_PROGRESS.md`
- [ ] Add `pyproject.toml`
- [ ] Configure Ruff
- [ ] Configure pytest
- [ ] Configure mypy/pyright
- [ ] Configure pre-commit
- [ ] Add `.env.example`
- [ ] Add `.gitignore`
- [ ] Create Makefile
- [ ] Add GitHub Actions CI
- [ ] Add basic health endpoint
- [ ] Add project architecture diagram

## Initial commands

```bash
mkdir graphops-ai
cd graphops-ai

git init

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
```

## Definition of done

```text
make lint
make test
make typecheck
```

all pass.

---

# 6. Phase 1 — Domain Model

Create framework-independent domain models.

## Entities

```text
Document
Chunk
Entity
Relationship
Source
RetrievalResult
Agent
AgentTask
InferenceRequest
InferenceResponse
EvaluationSample
EvaluationResult
GPUWorkload
```

## Example graph entity

```python
class Entity:
    id: str
    name: str
    type: str
    source_document_id: str
    confidence: float
```

## Relationship

```python
class Relationship:
    source_entity_id: str
    target_entity_id: str
    relation_type: str
    confidence: float
    evidence_chunk_id: str
```

## Acceptance criteria

- [ ] Domain models do not depend on FastAPI
- [ ] Unit tests cover validation
- [ ] IDs are stable
- [ ] Source/evidence provenance is retained

---

# 7. Phase 2 — Document Ingestion

Implement a small but realistic corpus.

## Initial sources

```text
Markdown
PDF
plain text
JSON
Git repositories
```

## Pipeline

```text
source
  ↓
parser
  ↓
normalized document
  ↓
metadata extraction
  ↓
chunking
  ↓
Chunk objects
```

## Chunk metadata

Every chunk should retain:

```json
{
  "document_id": "...",
  "chunk_id": "...",
  "source": "...",
  "title": "...",
  "section": "...",
  "page": 3,
  "content_hash": "...",
  "created_at": "..."
}
```

## Tasks

- [ ] Implement Markdown parser
- [ ] Implement text parser
- [ ] Implement PDF parser
- [ ] Implement JSON parser
- [ ] Add chunking strategy
- [ ] Preserve source metadata
- [ ] Add deterministic content hashes
- [ ] Add ingestion tests

## Definition of done

A source document can be transformed into deterministic chunks with provenance.

---

# 8. Phase 3 — Embedding Pipeline

## Objective

Create a model-independent embedding interface.

```python
class EmbeddingProvider(Protocol):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, text: str) -> list[float]:
        ...
```

## Tasks

- [ ] Integrate a small Hugging Face embedding model
- [ ] Implement batching
- [ ] Add embedding cache
- [ ] Persist embeddings
- [ ] Record model name/version
- [ ] Add embedding tests

## Important metadata

```text
embedding_model
embedding_dimension
model_revision
created_at
content_hash
```

---

# 9. Phase 4 — Vector Retrieval Baseline

Build a strong baseline before GraphRAG.

## Pipeline

```text
query
 ↓
query embedding
 ↓
vector search
 ↓
top-k
 ↓
reranking
 ↓
context
```

## Tasks

- [ ] Implement FAISS-backed vector index
- [ ] Implement top-k retrieval
- [ ] Add metadata filtering
- [ ] Add optional reranker
- [ ] Implement retrieval API
- [ ] Add retrieval unit tests
- [ ] Add benchmark dataset

## API

```http
POST /v1/retrieval/vector
```

Example:

```json
{
  "query": "Why did payment service fail?",
  "top_k": 8
}
```

## Definition of done

Vector RAG can answer baseline questions and returns source provenance.

---

# 10. Phase 5 — Knowledge Graph

This is the first major differentiator.

## Graph model

Recommended initial node types:

```text
Service
Team
Database
API
Repository
Deployment
Incident
Technology
Configuration
Document
Person
Environment
```

## Relationship types

```text
DEPENDS_ON
CALLS
DEPLOYED_ON
OWNED_BY
USES
AFFECTED_BY
CAUSED_BY
DOCUMENTED_IN
CONFIGURED_BY
RELATED_TO
```

## Example

```text
PaymentService
  ├── DEPENDS_ON → PostgreSQL
  ├── DEPENDS_ON → Redis
  ├── OWNED_BY → PaymentsTeam
  ├── DEPLOYED_ON → production
  └── AFFECTED_BY → Incident-042

Incident-042
  └── CAUSED_BY → RedisMemoryPressure
```

## Tasks

- [ ] Select graph database
- [ ] Create graph schema
- [ ] Implement entity repository
- [ ] Implement relationship repository
- [ ] Implement graph writer
- [ ] Implement graph queries
- [ ] Add provenance links
- [ ] Add graph consistency tests

## Important rule

Never store an extracted relationship without its evidence:

```text
relationship
    ↓
evidence chunk
    ↓
source document
```

This is important for explainability and evaluation.

---

# 11. Phase 6 — Entity and Relationship Extraction

## Pipeline

```text
Document
   ↓
Chunk
   ↓
LLM/Transformer extraction
   ↓
Entities
   +
Relationships
   ↓
Validation
   ↓
Knowledge Graph
```

## Extraction schema

```json
{
  "entities": [
    {
      "name": "PaymentService",
      "type": "Service"
    }
  ],
  "relationships": [
    {
      "source": "PaymentService",
      "relation": "DEPENDS_ON",
      "target": "Redis"
    }
  ]
}
```

## Tasks

- [ ] Define extraction schema
- [ ] Implement structured extraction
- [ ] Validate extracted entities
- [ ] Validate relationship endpoints
- [ ] Deduplicate entities
- [ ] Merge aliases
- [ ] Store confidence
- [ ] Store evidence chunk
- [ ] Add extraction tests

## Quality controls

- Schema validation
- Entity normalization
- Duplicate detection
- Relationship validation
- Confidence thresholds

---

# 12. Phase 7 — Graph Retrieval

Implement graph retrieval independently from vector retrieval.

## Retrieval modes

### Entity lookup

```text
query
 ↓
entity extraction
 ↓
entity lookup
 ↓
neighbors
```

### Relationship traversal

```text
entity
 ↓
1-hop
 ↓
2-hop
 ↓
filtered paths
```

### Path retrieval

Return:

```text
PaymentService
   ↓ DEPENDS_ON
Redis
   ↓ AFFECTED_BY
Incident-042
   ↓ CAUSED_BY
MemoryPressure
```

## Tasks

- [ ] Entity resolver
- [ ] Neighbor retrieval
- [ ] Multi-hop traversal
- [ ] Path scoring
- [ ] Evidence collection
- [ ] Graph context formatter
- [ ] Graph retrieval tests

---

# 13. Phase 8 — Hybrid GraphRAG

This is the core AI feature.

## Architecture

```text
                       Query
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Vector Retriever        Graph Retriever
             │                       │
             └───────────┬───────────┘
                         ▼
                    Candidate Pool
                         │
                         ▼
                      Reranker
                         │
                         ▼
                   Context Builder
                         │
                         ▼
                        LLM
```

## Candidate fusion

Implement at least:

```text
Reciprocal Rank Fusion
```

Optionally compare:

```text
weighted score fusion
cross-encoder reranking
graph path weighting
```

## Tasks

- [ ] Define retriever interface
- [ ] Implement vector retriever
- [ ] Implement graph retriever
- [ ] Implement fusion
- [ ] Implement reranking
- [ ] Implement context builder
- [ ] Add citation generation
- [ ] Add hybrid retrieval tests

## API

```http
POST /v1/rag/query
```

Example response:

```json
{
  "answer": "...",
  "sources": [],
  "graph_paths": [],
  "retrieval_mode": "hybrid"
}
```

---

# 14. Phase 9 — Hugging Face Transformer Layer

Create an explicit model abstraction.

```python
class GenerationProvider(Protocol):
    async def generate(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        ...
```

Implement:

```text
HFLocalProvider
VLLMProvider
RemoteProvider
```

## Hugging Face responsibilities

Use Transformers for:

- model/tokenizer loading
- local development inference where practical
- embeddings/reranking where appropriate
- model metadata
- model configuration

## Tasks

- [ ] Add model registry
- [ ] Add model metadata
- [ ] Implement tokenizer abstraction
- [ ] Implement generation interface
- [ ] Add local-small-model profile
- [ ] Add model health checks
- [ ] Add model configuration validation

---

# 15. Phase 10 — vLLM Serving

Move generation behind vLLM.

vLLM provides an OpenAI-compatible HTTP server and supports serving Hugging Face models; its current documentation also supports loading models through the Transformers backend. See the official documentation:

- https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/
- https://huggingface.co/docs/transformers/community_integrations/vllm

## Local deployment

Start with the smallest model that fits your hardware.

Example shape:

```bash
vllm serve <small-hf-model> \
  --gpu-memory-utilization 0.70
```

Tune the value experimentally rather than blindly copying a production default.

vLLM exposes `--gpu-memory-utilization`, and its documentation notes that increasing it can improve KV-cache capacity but excessive values can cause OOM. 

## API

```text
/v1/chat/completions
/v1/completions
```

## Tasks

- [ ] Create vLLM Docker profile
- [ ] Configure model cache
- [ ] Configure GPU memory budget
- [ ] Add health check
- [ ] Add OpenAI-compatible client
- [ ] Add timeout handling
- [ ] Add retry policy
- [ ] Add circuit breaker
- [ ] Add inference metrics
- [ ] Benchmark local serving

## Metrics

```text
TTFT
tokens/sec
request latency
p50
p95
p99
error rate
GPU memory
queue wait
```

---

# 16. Phase 11 — Model Router

Build an internal model router.

```text
                    Model Router
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
        local          vLLM        remote
         HF           server       provider
```

Routing rules:

```text
small request → local model
normal request → vLLM
large/complex request → remote model
```

Do not hard-code provider logic into the RAG engine.

## Tasks

- [ ] Define provider interface
- [ ] Implement provider registry
- [ ] Implement routing rules
- [ ] Implement fallback
- [ ] Add timeout handling
- [ ] Add request tracing
- [ ] Add model selection logs

---

# 17. Phase 12 — GPU Workload Scheduler

Do not pretend the laptop has a multi-GPU cluster.

Implement two layers:

### Layer A — local scheduler

Real scheduling queue:

```text
Request
   ↓
Priority Queue
   ↓
GPU availability
   ↓
vLLM
```

### Layer B — Kubernetes scheduler model

Represent future GPU nodes:

```text
GPU Node
  ├── memory
  ├── compute capability
  ├── model cache
  └── current utilization
```

Kubernetes exposes GPUs as schedulable device resources through device plugins, and GPU resources can be requested by Pods. See:

https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/

## Scheduling policies

Implement:

- [ ] FIFO
- [ ] Priority queue
- [ ] Weighted fair queue
- [ ] Maximum queue depth
- [ ] Timeout
- [ ] Retry
- [ ] Backpressure

## GPU-aware scheduling

A workload should carry:

```json
{
  "model": "small-model",
  "gpu_memory_required_mb": 2500,
  "priority": 5,
  "max_latency_ms": 5000
}
```

Scheduler decision:

```text
Can GPU satisfy request?
        │
      yes ──→ dispatch
        │
       no
        │
        ▼
queue / fallback / reject
```

## Metrics

```text
queue_wait_ms
dispatch_latency_ms
inference_latency_ms
throughput_tokens_sec
active_requests
rejected_requests
gpu_memory_used
```

---

# 18. Phase 13 — Kubernetes GPU Deployment

This phase is primarily an architecture/deployment demonstration.

## Components

```text
Kubernetes
├── API
├── Graph service
├── Retrieval service
├── Agent services
├── Scheduler
├── vLLM
└── Observability
```

## GPU Pod

```yaml
resources:
  limits:
    nvidia.com/gpu: 1
```

Kubernetes documents GPU scheduling as stable functionality and uses vendor device plugins such as NVIDIA's to expose resources like `nvidia.com/gpu`.

## Tasks

- [ ] Create namespace
- [ ] Create ConfigMaps
- [ ] Create Secrets template
- [ ] Create Deployments
- [ ] Create Services
- [ ] Create GPU workload manifest
- [ ] Add node selectors
- [ ] Add readiness probes
- [ ] Add liveness probes
- [ ] Add resource limits
- [ ] Add Helm chart
- [ ] Document remote-GPU deployment

## Local limitation

If the laptop cannot run a real GPU Kubernetes node, validate:

```text
manifest correctness
resource requests
scheduler behavior
service communication
```

and run the actual GPU workload directly through Docker/vLLM.

---

# 19. Phase 14 — A2A Multi-Agent Layer

A2A is the horizontal agent-to-agent interoperability layer.

Official A2A documentation describes it as an open standard for communication and collaboration between AI agents. A2A was donated to the Linux Foundation and, as of August 2026, is part of the Agentic AI Foundation ecosystem.

Reference:

https://a2a-protocol.org/

## Agents

### Research Agent

Responsibilities:

```text
find relevant evidence
retrieve documents
retrieve graph paths
summarize findings
```

### RCA Agent

Responsibilities:

```text
analyze incident
traverse dependencies
identify candidate causes
produce evidence-backed explanation
```

### Code Agent

Responsibilities:

```text
inspect repository information
connect incidents to code
identify potentially related components
```

### Evaluation Agent

Responsibilities:

```text
verify answer
check citations
measure evidence coverage
flag unsupported claims
```

---

# 20. A2A Agent Cards

Each agent should publish an Agent Card describing:

```text
name
description
capabilities
supported interfaces
endpoint
authentication
```

Example conceptual card:

```json
{
  "name": "RCA Agent",
  "description": "Analyzes technical incidents using GraphRAG.",
  "capabilities": [
    "incident-analysis",
    "dependency-analysis",
    "evidence-retrieval"
  ]
}
```

## Tasks

- [ ] Implement Agent Card
- [ ] Implement A2A server
- [ ] Implement A2A client
- [ ] Implement task submission
- [ ] Implement task status
- [ ] Implement result retrieval
- [ ] Implement agent discovery
- [ ] Add authentication abstraction
- [ ] Add agent timeout
- [ ] Add retries
- [ ] Add task tracing

---

# 21. Phase 15 — Agent Orchestration

Example request:

```text
"Why did PaymentService become slow after deployment 42?"
```

Orchestrator:

```text
1. Research Agent
   ↓
2. RCA Agent
   ↓
3. Code Agent
   ↓
4. Evaluation Agent
   ↓
5. Final response
```

## Orchestration graph

```text
User
 ↓
Orchestrator
 ├── Research Agent
 │      ↓
 │   evidence
 │
 ├── RCA Agent
 │      ↓
 │   causal paths
 │
 ├── Code Agent
 │      ↓
 │   code/deployment evidence
 │
 └── Evaluation Agent
        ↓
     validation
        ↓
     final answer
```

## Tasks

- [ ] Define agent task schema
- [ ] Implement orchestration
- [ ] Implement parallel execution where safe
- [ ] Implement dependency handling
- [ ] Implement timeout
- [ ] Implement partial failure handling
- [ ] Implement final evidence aggregation

---

# 22. Phase 16 — Evaluation Dataset

This is mandatory.

Create a versioned benchmark:

```text
evaluation/datasets/
├── queries.jsonl
├── expected_entities.jsonl
├── expected_sources.jsonl
├── expected_answers.jsonl
└── README.md
```

Each question should contain:

```json
{
  "id": "q001",
  "question": "Why did PaymentService fail?",
  "expected_entities": [
    "PaymentService",
    "Redis"
  ],
  "expected_sources": [
    "incident-042.md"
  ]
}
```

Start with:

```text
30–100 questions
```

Do not optimize for dataset size. Optimize for meaningful failure cases.

---

# 23. Phase 17 — Retrieval Evaluation

Compare:

```text
Vector RAG
GraphRAG
Hybrid GraphRAG
```

Metrics:

```text
Recall@K
Precision@K
MRR
nDCG
Context Recall
Context Precision
```

Experiment table:

```text
experiment_id
dataset_version
retriever
top_k
reranker
model
recall_at_5
precision_at_5
mrr
latency_ms
```

## Required experiment

Run the same evaluation set through:

```text
A. Vector only
B. Graph only
C. Hybrid
```

Store raw results.

---

# 24. Phase 18 — Generation Evaluation

Measure:

```text
Faithfulness
Answer relevance
Correctness
Citation accuracy
Unsupported claim rate
```

Also implement deterministic checks where possible.

Example:

```text
Every factual claim should map to:
    source document
       OR
    graph path
```

## Hallucination test

Create adversarial questions where the corpus does not contain enough information.

Expected behavior:

```text
"I don't have enough evidence to answer this."
```

rather than fabricated facts.

---

# 25. Phase 19 — End-to-End Evaluation

Test the entire system:

```text
Question
 ↓
Agent orchestration
 ↓
GraphRAG
 ↓
Model Router
 ↓
GPU Scheduler
 ↓
vLLM
 ↓
Answer
 ↓
Evaluation
```

Track:

```text
total latency
retrieval latency
graph latency
reranking latency
queue latency
TTFT
generation latency
tokens/sec
evaluation latency
```

Create trace IDs:

```text
request_id
 ├── agent_task_id
 ├── retrieval_id
 ├── inference_id
 └── evaluation_id
```

---

# 26. Phase 20 — Benchmarking GPU Scheduling

Create synthetic workloads:

```text
low priority
medium priority
high priority
```

Compare:

```text
FIFO
Priority
Weighted Fair Queue
```

Measure:

```text
average wait
p50 wait
p95 wait
throughput
starvation
deadline violations
```

Important:

Do not claim one scheduling algorithm is universally superior. Report your measured behavior under your workload.

---

# 27. Phase 21 — Observability

Implement:

```text
OpenTelemetry
Prometheus
Grafana
structured JSON logging
```

## Traces

Trace:

```text
HTTP request
 → A2A task
 → retrieval
 → graph query
 → model routing
 → scheduler
 → vLLM
 → evaluation
```

## Metrics

### API

```text
http_requests_total
http_request_duration_seconds
http_errors_total
```

### Retrieval

```text
retrieval_latency
retrieval_candidates
graph_hops
reranker_latency
```

### Inference

```text
inference_requests
ttft
tokens_per_second
inference_latency
```

### Scheduler

```text
queue_depth
queue_wait
dispatch_count
rejected_requests
```

### Evaluation

```text
faithfulness
relevance
citation_accuracy
retrieval_recall
```

---

# 28. Phase 22 — Reliability

Implement:

- [ ] request timeouts
- [ ] retry with exponential backoff
- [ ] circuit breaker
- [ ] idempotency keys
- [ ] dead-letter handling
- [ ] graceful shutdown
- [ ] health checks
- [ ] readiness checks
- [ ] model-unavailable fallback
- [ ] graph unavailable fallback
- [ ] vector index unavailable fallback

Example:

```text
Graph unavailable
       ↓
Vector RAG fallback
       ↓
Answer with reduced capability
       ↓
Clearly expose retrieval mode
```

---

# 29. Phase 23 — Security

Implement:

```text
API authentication
agent authentication abstraction
RBAC
rate limiting
request validation
secret management
audit logs
```

Do not expose vLLM directly to the public internet.

Put it behind the API/inference gateway.

---

# 30. Phase 24 — Docker Compose

Create profiles:

```text
default
cpu
gpu
observability
evaluation
```

Example:

```bash
docker compose --profile cpu up
docker compose --profile gpu up
docker compose --profile evaluation up
```

## Services

```text
api
ingestion
graph
retrieval
scheduler
agents
vllm
prometheus
grafana
```

Keep the default profile lightweight enough for the 8 GB RAM machine.

---

# 31. Phase 25 — CI/CD

GitHub Actions:

```text
push
 ↓
lint
 ↓
typecheck
 ↓
unit tests
 ↓
integration tests
 ↓
build Docker images
 ↓
security scan
```

Evaluation workflow:

```text
manual trigger
 ↓
evaluation dataset
 ↓
run benchmark
 ↓
compare baseline
 ↓
publish report
```

---

# 32. Phase 26 — Regression Testing

Create a retrieval/generation regression gate.

Example:

```text
if Recall@5 drops > threshold:
    fail evaluation

if citation accuracy drops > threshold:
    fail evaluation

if p95 latency increases > threshold:
    warn/fail depending on profile
```

Do not use arbitrary thresholds without documenting why they were chosen.

---

# 33. Phase 27 — Architecture Decision Records

Create:

```text
docs/adr/
├── 001-architecture.md
├── 002-vector-index.md
├── 003-graph-database.md
├── 004-hybrid-retrieval.md
├── 005-vllm.md
├── 006-gpu-scheduler.md
├── 007-a2a.md
└── 008-evaluation.md
```

Each ADR:

```text
Context
Decision
Alternatives
Trade-offs
Consequences
```

This is particularly useful during interviews.

---

# 34. Phase 28 — Final Demo Scenarios

The README must contain reproducible scenarios.

## Demo 1 — GraphRAG

```text
Ask:
"Which services depend on Redis and were affected by the incident?"
```

Show:

```text
entities
relationships
graph paths
sources
answer
```

## Demo 2 — Hybrid retrieval

Run:

```text
Vector
Graph
Hybrid
```

Show retrieval differences.

## Demo 3 — A2A

```text
User
 ↓
Orchestrator
 ↓
Research Agent
 ↓
RCA Agent
 ↓
Evaluation Agent
```

Show task IDs and agent messages.

## Demo 4 — vLLM

Show:

```text
request
 ↓
model router
 ↓
scheduler
 ↓
vLLM
 ↓
response
```

## Demo 5 — Evaluation

Show:

```text
Vector RAG vs GraphRAG vs Hybrid
```

with measured metrics.

## Demo 6 — GPU scheduling

Submit concurrent requests and visualize:

```text
queue
priority
wait time
execution
throughput
```

---

# 35. Phase 29 — Portfolio Dashboard

Build a simple UI.

Pages:

```text
Dashboard
Knowledge Graph
Documents
Graph Explorer
RAG Playground
Agents
A2A Tasks
Inference
GPU Scheduler
Evaluation
Observability
```

## RAG Playground

Show:

```text
Question
Retrieval mode
Sources
Graph paths
Answer
Latency
Model
Tokens/sec
```

## Evaluation page

Show:

```text
Dataset
Experiment
Retriever
Model
Recall
MRR
Faithfulness
Relevance
Latency
```

---

# 36. Phase 30 — Final Documentation

README sections:

```text
1. Problem
2. Architecture
3. Why GraphRAG
4. Knowledge Graph
5. Hybrid Retrieval
6. Hugging Face
7. vLLM
8. GPU Scheduling
9. A2A
10. Evaluation
11. Observability
12. Local Hardware
13. Deployment
14. Benchmarks
15. Trade-offs
16. Future Work
```

Include architecture diagrams.

---

# 37. Definition of Done

The project is portfolio-ready when all of these are true:

## Knowledge Graph

- [ ] Entities extracted
- [ ] Relationships extracted
- [ ] Provenance retained
- [ ] Multi-hop traversal works

## GraphRAG

- [ ] Vector retrieval works
- [ ] Graph retrieval works
- [ ] Hybrid retrieval works
- [ ] Reranking works
- [ ] Citations work

## Hugging Face

- [ ] Model registry exists
- [ ] Transformer model is integrated
- [ ] Provider abstraction exists

## vLLM

- [ ] Model served through vLLM
- [ ] OpenAI-compatible API works
- [ ] Health check works
- [ ] Metrics captured

## GPU Scheduling

- [ ] Queue exists
- [ ] Priority exists
- [ ] Resource-aware dispatch exists
- [ ] Scheduling benchmark exists
- [ ] Kubernetes GPU deployment manifests exist

## A2A

- [ ] Agent Cards exist
- [ ] A2A server works
- [ ] A2A client works
- [ ] Multiple agents collaborate
- [ ] Task state is observable

## Evaluation

- [ ] Benchmark dataset exists
- [ ] Vector baseline measured
- [ ] GraphRAG measured
- [ ] Hybrid measured
- [ ] Generation quality measured
- [ ] Regression tests exist

## Engineering

- [ ] Docker
- [ ] CI
- [ ] Tests
- [ ] Observability
- [ ] Security basics
- [ ] ADRs
- [ ] Architecture documentation

---

# 38. Recommended Implementation Order

Do NOT implement everything simultaneously.

Use this exact sequence:

```text
01. Repository bootstrap
        ↓
02. Domain models
        ↓
03. Document ingestion
        ↓
04. Embeddings
        ↓
05. Vector RAG baseline
        ↓
06. Evaluation dataset
        ↓
07. Knowledge Graph
        ↓
08. Entity/relationship extraction
        ↓
09. Graph retrieval
        ↓
10. Hybrid GraphRAG
        ↓
11. Hugging Face model layer
        ↓
12. vLLM
        ↓
13. Model Router
        ↓
14. GPU Scheduler
        ↓
15. A2A agents
        ↓
16. Agent orchestration
        ↓
17. End-to-end evaluation
        ↓
18. Observability
        ↓
19. Kubernetes/Helm
        ↓
20. Dashboard
        ↓
21. Benchmark report
        ↓
22. Portfolio documentation
```

---

# 39. Milestone Strategy

## Milestone 1 — Working RAG

```text
Document → chunks → embeddings → vector search → LLM
```

Status:

- [ ] Complete

## Milestone 2 — GraphRAG

```text
Documents → KG
             +
Vector DB
             ↓
Hybrid retrieval
```

Status:

- [ ] Complete

## Milestone 3 — Production inference

```text
HF model → vLLM → model router
```

Status:

- [ ] Complete

## Milestone 4 — AI infrastructure

```text
Requests → GPU scheduler → inference
```

Status:

- [ ] Complete

## Milestone 5 — Multi-agent

```text
A2A orchestrator → specialized agents
```

Status:

- [ ] Complete

## Milestone 6 — Evaluation

```text
dataset → experiments → metrics → regression
```

Status:

- [ ] Complete

## Milestone 7 — Production engineering

```text
Kubernetes
Observability
Security
CI/CD
```

Status:

- [ ] Complete

---

# 40. Stretch Goals

Only implement these after the core project works.

## Advanced GraphRAG

- [ ] Community detection
- [ ] Community summaries
- [ ] Global search
- [ ] Graph-aware reranking
- [ ] Temporal graph queries

## Advanced inference

- [ ] Prefix caching
- [ ] Request batching
- [ ] Speculative decoding experiments
- [ ] Model fallback
- [ ] Multi-model routing

## Advanced scheduling

- [ ] SLA-aware scheduling
- [ ] GPU memory prediction
- [ ] Model-aware queueing
- [ ] Fair-share scheduling
- [ ] Admission control

## Advanced agents

- [ ] Dynamic agent discovery
- [ ] Agent capability matching
- [ ] Parallel agent execution
- [ ] Human approval workflow
- [ ] Long-running A2A tasks

## Advanced evaluation

- [ ] Synthetic benchmark generation
- [ ] Human evaluation interface
- [ ] LLM-as-judge comparison
- [ ] Retrieval regression CI
- [ ] Cost-quality-latency optimization

---

# 41. What NOT to Do

Avoid:

```text
❌ giant local models
❌ huge document datasets
❌ unnecessary microservices from day one
❌ hiding everything behind LangChain
❌ fake GPU cluster screenshots
❌ invented benchmark numbers
❌ claiming production scale from a laptop
❌ implementing A2A only as a renamed REST endpoint
❌ measuring only "the answer looks good"
```

Instead:

```text
✓ small reproducible dataset
✓ real measurements
✓ clear interfaces
✓ explicit trade-offs
✓ evidence-backed answers
✓ constrained-hardware profile
✓ scalable architecture
```

---

# 42. Final Resume Positioning

After implementation, the project should support resume bullets like:

> **GraphOps AI — GraphRAG Multi-Agent AI Platform:** Engineered a production-style AI platform combining knowledge graphs, vector retrieval, hybrid GraphRAG, Hugging Face Transformers, and evidence-backed generation for technical knowledge discovery.

> **AI Inference Infrastructure:** Built a model-serving layer using vLLM with OpenAI-compatible inference, model routing, GPU-aware workload scheduling, queue management, and latency/throughput instrumentation.

> **Agentic AI & Evaluation:** Implemented A2A-based collaboration between specialized research, RCA, coding, and evaluation agents, with automated retrieval/generation benchmarks and regression testing.

Only add numerical metrics after running the experiments and recording the actual results.

---

# 43. Interview Topics This Project Should Prepare You For

Be able to explain:

### RAG

- Why vector RAG fails on relational questions
- Chunking trade-offs
- Embedding model selection
- Reranking
- Context limits

### GraphRAG

- Entity extraction
- Relationship extraction
- Graph traversal
- Path scoring
- Graph vs vector retrieval
- Hybrid fusion

### Transformers

- Tokenization
- Attention
- KV cache
- Quantization
- Inference vs training

### vLLM

- Continuous batching
- KV cache
- GPU memory
- Serving architecture
- OpenAI-compatible API

### GPU Scheduling

- Resource requests
- Queueing
- Fairness
- Backpressure
- Admission control
- Kubernetes device plugins

### A2A

- Agent Cards
- Task lifecycle
- Agent discovery
- Agent interoperability
- A2A vs MCP

### Evaluation

- Recall@K
- MRR
- nDCG
- Faithfulness
- Relevance
- Hallucination
- Regression testing

### AI System Design

- Failure modes
- Scaling
- observability
- cost
- latency
- security
- model fallback

---

# 44. Official Technical References

Use these as the primary references while implementing:

- A2A Protocol: https://a2a-protocol.org/
- vLLM OpenAI-compatible server: https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/
- vLLM serving CLI: https://docs.vllm.ai/en/stable/cli/serve/
- Hugging Face Transformers + vLLM: https://huggingface.co/docs/transformers/community_integrations/vllm
- Kubernetes GPU scheduling: https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/
- Kubernetes device plugins: https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/

---

# 45. Current Status

## Overall

**0% — Not started**

## Phase status

| Phase | Component | Status |
|---|---|---|
| 0 | Repository bootstrap | ⬜ |
| 1 | Domain model | ⬜ |
| 2 | Document ingestion | ⬜ |
| 3 | Embeddings | ⬜ |
| 4 | Vector RAG baseline | ⬜ |
| 5 | Knowledge graph | ⬜ |
| 6 | Entity/relationship extraction | ⬜ |
| 7 | Graph retrieval | ⬜ |
| 8 | Hybrid GraphRAG | ⬜ |
| 9 | Hugging Face layer | ⬜ |
| 10 | vLLM serving | ⬜ |
| 11 | Model router | ⬜ |
| 12 | GPU scheduler | ⬜ |
| 13 | Kubernetes GPU deployment | ⬜ |
| 14 | A2A | ⬜ |
| 15 | Agent orchestration | ⬜ |
| 16 | Evaluation dataset | ⬜ |
| 17 | Retrieval evaluation | ⬜ |
| 18 | Generation evaluation | ⬜ |
| 19 | End-to-end evaluation | ⬜ |
| 20 | Scheduling benchmarks | ⬜ |
| 21 | Observability | ⬜ |
| 22 | Reliability | ⬜ |
| 23 | Security | ⬜ |
| 24 | Docker Compose | ⬜ |
| 25 | CI/CD | ⬜ |
| 26 | Regression testing | ⬜ |
| 27 | ADRs | ⬜ |
| 28 | Demo scenarios | ⬜ |
| 29 | Portfolio dashboard | ⬜ |
| 30 | Final documentation | ⬜ |

---

# 46. Golden Rule

Build the project in this order:

```text
WORKING
   ↓
MEASURED
   ↓
OPTIMIZED
   ↓
DISTRIBUTED
   ↓
PRODUCTION-ENGINEERED
```

Do not start with Kubernetes, multi-agent orchestration, or GPU scheduling.

First make the **GraphRAG system correct and measurable**.

Then make inference efficient.

Then add agents.

Then demonstrate infrastructure scaling.

That produces a much stronger AI Software Engineer portfolio story.
