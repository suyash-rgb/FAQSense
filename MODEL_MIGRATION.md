# Model Migration & Tuning Documentation

## Overview
This document outlines the migration of the FAQSense backend from the legacy `sentence-transformers` (all-MiniLM-L6-v2) to the high-performance **FastEmbed** framework using the `BAAI/bge-small-en-v1.5` model.

The primary goals of this migration were:
1. **Performance**: Reducing backend startup time and memory footprint.
2. **Accuracy**: Leveraging a more modern model with higher semantic reasoning capabilities.
3. **Robustness**: Tuning metrics to handle the higher-density score distribution of the BGE model.

---

## 1. Architectural Changes

### Lazy Loading & FastEmbed
- **Legacy**: Loaded the model on startup, causing a ~5-10 second delay before the API was ready.
- **New**: Implemented **Lazy Loading** in `engine_service.py`. The model is only initialized when the first query arrives.
- **Library**: Switched from `sentence-transformers` (PyTorch-heavy) to `fastembed`, which uses ONNX Runtime for significantly faster CPU inference and lower RAM usage.

### Keyword Normalization
We updated the keyword extraction logic to handle simple plurals.
- **Fix**: Words longer than 3 characters ending in 's' are normalized (e.g., "refunds" becomes "refund").
- **Benefit**: Ensures "refund" (query) matches "refunds" (CSV) in the Faithfulness Guardrail checks.

---

## 2. Metric Tuning for BGE-small-en-v1.5

The BGE model produces a tighter, higher-scoring distribution compared to MiniLM. Using legacy thresholds caused significant "False Positives" and "Ambiguity Traps."

| Metric | Legacy (MiniLM) | New (BGE-Small) | Reasoning |
| :--- | :--- | :--- | :--- |
| **Semantic Match Threshold** | 0.35 | **0.50** | Prevents matched answers for unrelated queries. |
| **Confidence Threshold** | 0.60 | **0.75** | The score is required to bypass keyword overlap (Synonym trust). |
| **Ambiguity Threshold** | 0.15 | **0.03** | Adjusted for the denser score gap in BGE. |
| **Bypass Ambiguity** | N/A | **0.92** | If the semantic score is > 0.92, we trust it as a near-perfect match. |

### Variant-Aware Ambiguity (Post-Migration Fix)
We updated the `Ambiguity Guard` to be "Variant-Aware." 
- **The Issue**: Previously, having two similar questions (variants) pointing to the same answer would trigger the ambiguity fallback because the "Score Gap" was too small.
- **The Fix**: The system now compares the **Answers** of the top two results. If the scores are close but the answers are **identical**, the system allows the match. It only fallbacks if the top results point to **different** answers.
- **Benefit**: Supports the React-Flow frontend strategy of adding multiple question variant nodes to a single answer node.

---

## 3. Query LifeCycle: Verified Logic

We verified the 5-phase lifecycle through comprehensive integration testing:

1.  **Phase 1: Arrival (Clean Wall)**: Verified that Bot A cannot see Bot B's data via filepath isolation.
2.  **Phase 2: Exact Match**: Verified case-insensitive/whitespace-insensitive matching.
3.  **Phase 3: Fuzzy Match**: Verified typo handling (e.g., "refinds" → "refunds").
4.  **Phase 4: Semantic Search**: Verified intent matching (e.g., "money back" → "refunds").
5.  **Phase 5: Safety Guardrails**:
    - **Keyword Guard**: Rejects generic queries (e.g., "Tell me about finances") even if the semantic score is moderately high, unless keyword overlap exists.
    - **Ambiguity Guard**: Prevents "guessing" when two FAQ questions are semantically too close.

---

## 4. Operational Observations
- **Startup Time**: < 100ms (Down from ~8s).
- **First-Query Latency**: ~1.5s (Model init overhead).
- **Subsequent Queries**: < 50ms.
- **Memory Footprint**: Significantly reduced due to ONNX Runtime optimizations.

**Date of implementation:** February 27, 2026




