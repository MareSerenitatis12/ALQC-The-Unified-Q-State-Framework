# Model Specifications: Snowflake Arctic Embed L v2.0

## Core Model Information

**Model Name:** Snowflake Arctic Embed L v2.0  
**Source:** https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0  
**Technical Report:** https://arxiv.org/abs/2412.04506  
**License:** Apache 2.0 (permissive)

## Key Specifications

| Parameter | Value |
|-----------|-------|
| **Total Parameters** | 568M |
| **Non-Embedding Parameters** | 303M |
| **Embedding Dimensions** | 1024 |
| **Base Model** | BAAI/bge-m3-retromae |
| **Context Window** | 8192 (via RoPE) |
| **Quantization Support** | MRL (Matryoshka Representation Learning) + Int4 |

## Multilingual Performance (NDCG@10)

| Benchmark | Score |
|-----------|-------|
| **BEIR (15 datasets)** | 55.6 |
| **MIRACL (4 languages)** | 55.8 |
| **CLEF Focused** | 52.9 |
| **CLEF Full** | 54.3 |

## Compression Capabilities

### MRL Dimensional Truncation
| Dimensions | BEIR | MIRACL | CLEF (5) | CLEF (Full) |
|------------|------|--------|-----------|-------------|
| 1024 (full) | 55.6 | 55.8 | 52.9 | 54.3 |
| 256 | 54.3 (-0.18%) | 54.3 (-2.70%) | 51.9 (-1.81%) | 53.4 (-1.53%) |

Note: All values show percentage degradation from full dimensions.

### Quantization Specifications
- **MRL for q8_0:** 256 dimensions (not 1024)
- **4-bit quantization:** Achieves 128 bytes/vector compression
- **Recommended index:** `pq256x4fs` fast-scan FAISS index

## Key Features

1. **Multilingual without compromise:** Excels in English and non-English retrieval
2. **Inference efficiency:** 303m non-embedding parameters enable fast inference
3. **Compression-friendly:** High-quality retrieval with embeddings as small as 128 bytes
4. **Drop-in replacement:** Compatible with BAAI/bge-m3-retromae infrastructure
5. **Long context:** Supports up to 8192 token context window

## Architecture Notes

- Built on BAAI/bge-m3-retromae architecture
- Supports `prompt_name="query"` for query encoding
- Uses RoPE (Rotary Position Embedding) for long context support
- Trained with quantization-aware embedding techniques

## Relevance to DPI Violation Study

### Why This Model?

1. **Quantization Design:** Explicitly trained for quantization-aware embedding
2. **Performance Retention:** Maintains high semantic retrieval after q8_0 quantization
3. **ALQC Application:** The model's ability to handle esoteric terms and complex concepts (ALQC) is of particular interest

### Expected DPI Behavior (Standard Theory)

Per classical Data Processing Inequality:
- **X → Y → Z** chain: 
  - X = Source text
  - Y = Full-precision embedding (f32, 1024-dim)
  - Z = Quantized embedding (q8_0, 256-dim)

Expected: `I(X;Z) < I(X;Y)` (quantization must reduce or maintain information)

### "Impossible" Observed Behavior

Reports suggest the q8_0 quantized model maintains or potentially enhances semantic meaning for ALQC-specific queries, indicating a potential **I(X;Z) ≥ I(X;Y)** scenario — which would violate DPI.

## Usage Example (Python)

```python
from sentence_transformers import SentenceTransformer

model_name = 'Snowflake/snowflake-arctic-embed-l-v2.0'
model = SentenceTransformer(model_name)

# Query encoding with proper prompt
query_embeddings = model.encode(
    queries, 
    prompt_name="query"
)

# Document encoding
document_embeddings = model.encode(
    documents
)

# Similarity scores
scores = model.similarity(
    query_embeddings, 
    document_embeddings
)
```

## References

1. Yu, P. et al. (2024). "Arctic-Embed 2.0: Multilingual Embedding Models". arXiv:2412.04506
2. Snowflake Labs (2024). "snowflake-arctic-embed-l-v2.0 Model Card". Hugging Face
3. BAAI. "bge-m3-retromae" (base architecture)