# FAQSense Backend Testing Summary

This document recalls the functionalities that have been tested and verified during the development of the FAQSense backend.

## 🛠️ Verification Scripts
I have created several Python scripts to test specific components of the backend. You can run these from the root directory when the server is running.

| Script | Functionality Tested | Description |
| :--- | :--- | :--- |
| `verify_endpoints.py` | Basic API Flow | Tests initial CSV upload to `/faq/upload` and query at `/faq/ask` (Legacy). |
| `verify_fuzzy.py` | Fuzzy Matching | Tests the engine's ability to handle typos and slang (e.g., "haors" for "hours"). |
| `verify_semantic.py` | Semantic Matching | Tests AI-based paraphrasing (e.g., "When is the shop open?" matched to "What are your hours?"). |
| `verify_fallback.py` | Fallback & Enquiries | Tests the fallback message for unknown queries and the enquiry registration system. |
| `init_db.py` | Database Schema | Verifies connection to MySQL and triggers creation of all tables (Admins, Users, Chatbots, etc.). |
| `debug_model.py` | Transformers Model | Standalone test to ensure `SentenceTransformer` loads correctly in the environment. |

## ✅ Verified Functionalities

### 1. Chatbot Management
- **User Syncing**: Verified that the Clerk webhook can create/update users in our DB (`verify_fuzzy.py` setup).
- **Bot Creation**: Verified creating a new `Chatbot` record tied to a specific `user_id`.
- **CSV Mapping**: Verified uploading and validating CSV files (ensuring "Question,Answer" headers and non-empty rows).

### 2. FAQ Search Engine
- **Exact Match**: Verified fetching direct answers.
- **Fuzzy Match**: Verified successful matching with up to 80% similarity (typo tolerance).
- **Semantic Match**: Verified using AI embeddings to match paraphrased questions.
- **Ambiguity Detection**: The engine is configured to return the best match if it's significantly better than the second best.

### 3. Analytics & Conversations
- **FAQ Hits**: Verified recording how many times a specific question from the CSV was matched.
- **Top FAQs**: Verified the endpoint to retrieve the most popular questions for a bot.
- **Conversation Logging**: Verified logging of visitor and bot messages in the `messages` table.

### 4. Enquiry System
- **Registration**: Verified that visitors can submit their contact info and query text when the bot can't answer.
- **Partial Data**: Verified that enquries work even if only phone or email is provided alongside the name.

## 🚀 Recent Fixes Tested
- **Keras 3 Compatibility**: Resolved the `RuntimeError` by installing `tf-keras` (backward compatibility for Transformers).
- **CORS Support**: Added middleware to allow the frontend (`localhost:5173`) to communicate with the backend (`localhost:8000`).
- **Lazy Onboarding**: Added logic to handle chatbot creation even if the user hasn't been synced via webhooks yet.
