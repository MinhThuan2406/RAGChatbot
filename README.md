# RAGChatbot

## A Small Side Project Utilizing Docker, Ngrok, and Other Utilities to Build a Local Chatbot

---

### 📌 Project Status
The project section is currently under review by **Anh Khiêm**. While waiting, it's recommended to explore the following key concepts and technologies to prepare for implementation.

---

### 🧠 Topics to Explore

#### 1. **FastAPI & Flask**
- Build APIs to serve responses from LLMs.
- Allow integration with frontend clients.
- Support multiple endpoints and request types for inference.

#### 2. **OOP & Design Patterns**
- Write flexible, maintainable code using principles like SOLID.
- Support interchangeable components (e.g., OpenAI, Anthropic, Ollama).
- Encapsulate logic for:
  - LLM providers
  - Embedding services
  - Vector databases
  - Routing and fallback mechanisms

#### 3. **Streamlit & OpenWebUI**
- Rapidly prototype interactive user interfaces for LLM applications.
- Connect backend APIs to the frontend with minimal effort.
- Support chat history, user inputs, and debug outputs.

#### 4. **Docker**
- Containerize all services for isolated and reproducible environments.
- Use `docker-compose` for managing dependencies and orchestration.
- Enable fast deployment and teardown.

#### 5. **Vector Databases**
- Learn to configure and use:
  - **Simple**: ChromaDB (lightweight, file-based)
  - **Advanced**: Supabase/PostgreSQL with pgvector extension
- Store embeddings and documents for RAG-based querying.

---

### 🚀 Final Project Goals: RAG-Based Chatbot

Once the foundational skills are covered, build a complete Retrieval-Augmented Generation chatbot system with the following **project criteria**:

#### ✅ Functional Requirements
- Accurate answers using RAG from stored documents.
- All services must be containerized using Docker.
- Deployable through **NGROK** for quick access.
- User-friendly **web interface** (via Streamlit/OpenWebUI).
- Backend API served through **FastAPI** or **Flask**.
- Clean, modular, and extensible codebase with best practices.

#### 🗂 Project Components
- **LLM API Wrapper** (OpenAI, Ollama, etc.)
- **Document Uploader & Indexer** (PDFs, Markdown, etc.)
- **Vector Store Manager** (Chroma/Supabase)
- **Query Router** (LLM + retriever logic)
- **Frontend Interface** (chat history, input/output display)
- **Docker & Deployment** (Dockerfile, docker-compose, ngrok)

---

### ✅ Success Criteria
- 📦 Fully containerized system
- 💬 Chatbot can respond correctly to domain-specific queries
- 🌐 Accessible via public URL (Ngrok tunnel)
- 🧼 Code follows clean architecture principles
- 📁 Well-documented repository and modular design

---
