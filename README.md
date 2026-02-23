# FAQSense.ai 🤖

![FAQSense Banner](https://img.shields.io/badge/FAQSense-AI--Powered--Knowledge--Management-blueviolet?style=for-the-badge&logo=probot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)

**FAQSense** is a state-of-the-art, AI-powered FAQ management platform designed to transform how businesses interact with their customers. By leveraging advanced semantic search and hybrid matching algorithms, FAQSense ensures that user queries are answered with human-like precision, reducing support overhead and improving user satisfaction.

---

## 🔥 Features

### 🧠 Intelligent Hybrid Search Engine
Most bots fail because they rely on exact keyword matches. FAQSense uses a triple-layered approach:
- **Exact Matching**: Instant retrieval for verbatim queries.
- **Fuzzy Matching**: High tolerance for typos and grammatical errors using `Rapidfuzz`.
- **Semantic search**: Powered by `Sentence-Transformers` (AI), the engine understands the *intent* behind a question, even if no keywords match.

### 📊 Advanced Analytics & Insights
- **Hit Tracking**: Monitor which FAQs are performing best.
- **Top Questions**: Identify trending user concerns automatically.
- **Conversation Logs**: Review full chat histories to identify knowledge gaps.

### 📁 Knowledge Base Management
- **Bulk Upload**: Seamlessly import your existing FAQs via CSV files.
- **Custom Personas**: Create multiple chatbots, each with its own niche knowledge base and personality.

### 📥 Enquiry Management
- **Human-in-the-loop**: Queries that the AI can't answer are automatically routed to an Enquiry Inbox for manual review, ensuring no customer is left unheard.

### 🔐 Enterprise-Grade Security
- **Clerk Integration**: Secure, modern authentication out of the box.

---

## 🛠 Tech Stack

### Frontend
- **Framework**: React 19 (Vite)
- **Styling**: Tailwind CSS & Vanilla CSS
- **State Management**: React Hooks
- **Authentication**: Clerk
- **Visuals**: ReactFlow (Knowledge visualization)
- **API Client**: Axios

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: SQLAlchemy (MySQL/SQLite Support)
- **AI/ML**: 
  - `Sentence-Transformers` (Embeddings)
  - `Torch` (Inference)
  - `Rapidfuzz` (String matching)
- **Validation**: Pydantic v2

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL (Optional, default is SQLite in برخی configs)

### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and provide your DATABASE_URL and CLERK secret keys

# Initialize database
python init_db.py

# Start the server
uvicorn app.main:app --reload
```
The backend will be available at `http://localhost:8000`.

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment variables
# Create a .env.local file with:
# VITE_CLERK_PUBLISHABLE_KEY=your_clerk_key

# Start the development server
npm run dev
```
The frontend will be available at `http://localhost:5173`.

---

## 📂 Project Structure

```text
FAQSense/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # Configuration & constants
│   │   ├── models/       # Database schemas
│   │   ├── services/     # Engine & logic (The AI "Brain")
│   │   └── main.py       # FastAPI entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Main route views
│   │   ├── utils/        # API helpers
│   │   └── App.jsx
│   └── package.json
└── README.md
```

---

## 🎯 Our Aim
The primary aim of FAQSense is to bridge the gap between static FAQ pages and expensive, complex customer support systems. We believe every business, regardless of size, deserves an AI that actually *understands* its customers.

---

## 🤝 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---

Made with ❤️ for the future of customer support.
