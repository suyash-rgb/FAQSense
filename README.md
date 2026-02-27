# FAQSense: Intelligent Multi-Tenant FAQ Automation Platform

FAQSense is an AI-powered high-performance, multi-tenant chatbot engine designed to provide instant, reliable customer support. By leveraging a Retrieval-Augmented Matcher (RAM) architecture. It allows multiple organizations to upload their proprietary FAQ data and instantly deploy customized, context-aware chatbots that are guaranteed to remain faithful to the source material. It features a visual flow editor for managing FAQ data and a robust hybrid search engine for answering queries.

![Landing Page](https://github.com/suyash-rgb/FAQSense/blob/2df83196cbbe716b5102864e0e78bc6760a9f5f8/img/landingpage1.png)

## About the Application

### Background & Motivation
In the current AI landscape, Large Language Models (LLMs) often suffer from “hallucinations”—generating confident but factually incorrect information. For businesses, this is a significant liability, as misinformation can erode trust and lead to costly mistakes. FAQSense was born out of the need for a solution that provides the natural feel of AI interaction without the risk of unreliable outputs.
While LLMs are powerful and can perform heavy lifting tasks such as semantic similarity search or contextual matching, relying on them exclusively introduces fragility. Our motivation is to design a system that does not depend on them for core functionality. By combining deterministic methods, curated knowledge bases, and lightweight NLP techniques, FAQSense aims to deliver consistent, trustworthy answers while still offering the conversational fluidity users expect from modern AI systems.

### Main Objective
The primary goal is to provide a low-latency, scalable infrastructure where "Knowledge Retrieval" is the priority. FAQSense ensures that a company's support bot only speaks from the provided "textbook" (CSV data), ensuring 100% factual consistency.

### Why it Matters
In the NLP domain, FAQSense demonstrates that Semantic Search (understanding meaning) can be more valuable than Generative Text for closed-domain applications like customer service. It showcases the practical application of high-dimensional vector embeddings and efficient similarity scoring in a production environment.


## 🚀 Key Features

- **Visual FAQ Management**: A React-Flow based dashboard that allows users to map questions to answers visually, supporting multiple "Question Variants" for a single answer. <br><br>
- **Zero-Hallucination Architecture**: Unlike GPT-based bots, FAQSense selects existing answers rather than generating new ones. <br><br>
- **Hybrid Search Engine**: A 5-phase query lifecycle that ensures accurate delivery: <br>
  1. **Exact Match**: Instant response for perfect string matches.
  2. **Fuzzy Search**: Robust handling of user errors via Levenshtein distance-based fuzzy matching.
  3. **Semantic Search**: Understands user intent using the **FastEmbed (BGE-Small)** model.
  4. **Faithfulness Guards**: Keyword reranking and ambiguity checks to prevent "hallucinations."
  5. **Confidence Reranking**: Adaptive thresholds based on model confidence. <br><br>
- **Multi-Tenant Isolation**: Secure data partitioning ensures that Organization A’s bot can never access Organization B’s data. <br><br>
- **Optimized for Deployment**: Leveraging FastEmbed and ONNX Runtime for <100ms startup times and minimal RAM usage on platforms like Render. <br><br>

## 🛠️ Technology Stack

- **Frontend**: React, React-Flow, TailwindCSS.
- **Backend**: FastAPI, SQLAlchemy (MySQL/PostgreSQL), FastEmbed.
- **Persistence**: Hybrid Storage (Database for metadata + CSV for FAQ data with atomic-swap updates).
- **Authentication**: Clerk.

## 📁 Repository Structure

This repository is organized into specific branches for development and deployment:
- `main`: (Current) Documentation and project overview.
- `frontend`: FAQSense Platform for instantly buidling, deployment, analytics and maintenance of chatbots. 
- `backend`: Core backend logic and API services.
- `backend-prod`: Production-optimized backend branch with Sentence-Transformers. 
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
