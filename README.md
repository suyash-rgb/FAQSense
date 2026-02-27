# FAQSense

FAQSense is an AI-powered FAQ management and chatbot platform designed to help businesses automate customer support with high precision and low latency. It features a visual flow editor for managing FAQ data and a robust hybrid search engine for answering queries.

## 🚀 Key Features

- **Visual FAQ Management**: A React-Flow based dashboard that allows users to map questions to answers visually, supporting multiple "Question Variants" for a single answer.
- **Hybrid Search Engine**: A 5-phase query lifecycle that ensures accurate delivery:
  1. **Exact Match**: Instant response for perfect string matches.
  2. **Fuzzy Search**: Handles typos and spelling variations using `token_set_ratio`.
  3. **Semantic Search**: Understands user intent using the **FastEmbed (BGE-Small)** model.
  4. **Faithfulness Guards**: Keyword reranking and ambiguity checks to prevent "hallucinations."
  5. **Confidence Reranking**: Adaptive thresholds based on model confidence.
- **"Clean Wall" Isolation**: Enterprise-grade data isolation ensuring `chatbot_id` specific data loading.
- **Optimized for Deployment**: Leveraging FastEmbed and ONNX Runtime for <100ms startup times and minimal RAM usage on platforms like Render.

## 🛠️ Technology Stack

- **Frontend**: React, React-Flow, TailwindCSS.
- **Backend**: FastAPI, SQLAlchemy (MySQL/PostgreSQL), FastEmbed.
- **Persistence**: Hybrid Storage (Database for metadata + CSV for FAQ data with atomic-swap updates).
- **Authentication**: Clerk.

## 📁 Repository Structure

This repository is organized into specific branches for development and deployment:
- `main`: (Current) Documentation and project overview.
- `backend`: Core backend logic and API services.
- `backend-opt-prod`: Production-optimized backend branch with FastEmbed and tuned metrics.

---

## 📈 Search Optimization & Tuning

The system has been recently migrated from `sentence-transformers` to `fastembed`, resulting in significant performance gains. 

| Metric | Optimized Value |
| :--- | :--- |
| **Search Model** | BAAI/bge-small-en-v1.5 |
| **Semantic Threshold** | 0.50 |
| **Ambiguity Gap** | 0.03 (Variant-Aware) |
| **Confidence Bypass** | 0.75 |

For detailed information on the model migration and metric tuning, refer to the `MODEL_MIGRATION.md` file in the `backend-opt-prod` branch.

---

© 2026 FAQSense Team. All rights reserved.
