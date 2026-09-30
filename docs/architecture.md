# GraphOps AI architecture

```mermaid
flowchart TD
    client[Web client] --> api[API gateway]
    api --> agents[A2A agent router]
    agents --> graphrag[GraphRAG engine]
    graphrag --> vector[Vector index]
    graphrag --> graph[Knowledge graph]
    graphrag --> context[Context builder and reranker]
    context --> router[Model router]
    router --> scheduler[GPU workload scheduler]
    scheduler --> serving[vLLM / Hugging Face serving]
    eval[Evaluation and observability] -.-> graphrag
    eval -.-> serving
```

The initial service is intentionally small: the API is a liveness boundary and
does not own retrieval, graph, model-serving, or agent logic. Those capabilities
will be added as independent modules in later phases.
