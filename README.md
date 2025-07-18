# RAGChatbot

A modular, containerized Retrieval-Augmented Generation (RAG) chatbot stack using FastAPI, ChromaDB, Ollama, and a modern web UI. Easily deployable locally or for remote access via Ngrok.

---

## 🚦 Project Status

This project is under active development. Contributions and feedback are welcome!

---

## 🏗️ Architecture Overview

- **Backend API:** FastAPI (serves chat and ingest endpoints)
- **Vector Store:** ChromaDB (stores document embeddings)
- **LLM Provider:** Ollama (local LLM inference)
- **Frontend:** Open WebUI or Streamlit (user chat interface)
- **Orchestration:** Docker Compose (all services containerized)
- **Remote Access:** Ngrok (optional, for public URLs)

---


## 🚀 Quick Start

See [USER_GUIDE.md](USER_GUIDE.md) for end-user instructions.
See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for developer setup.

---

---

## 🧩 Features

- Retrieval-augmented answering from your own documents
- Modular backend with clear separation of concerns
- Pluggable LLM and vector DB providers
- Modern, responsive web UI (Open WebUI or Streamlit)
- Fully containerized for easy deployment and teardown

---

## 🗂 Project Structure

- `backend/app/` – FastAPI backend (API, ingestion, core logic)
- `open-webui/` – Web UI (Open WebUI)
- `docker/` – Dockerfiles and compose files
- `README.Docker.md` – Docker & deployment guide

---

## 🛠️ Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Ngrok](https://ngrok.com/) (optional, for remote access)

---


## 📝 Documentation

- **User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
- **Developer Guide:** [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Deployment & Docker:** [README.Docker.md](README.Docker.md)
- **Web UI:** [open-webui/README.md](open-webui/README.md)
- **Changelog:** [open-webui/CHANGELOG.md](open-webui/CHANGELOG.md)

---

## 🧠 Topics to Explore

- FastAPI & Flask for backend APIs
- OOP & design patterns for modular code
- Streamlit & OpenWebUI for rapid UI prototyping
- Docker for reproducible environments
- Vector databases (ChromaDB, Supabase/pgvector)

---

## 🧪 Troubleshooting & FAQ

- **CORS errors:** Ensure frontend and backend URLs are correctly set in CORS config.
- **Service not starting:** Check logs with `docker compose logs -f`.
- **Port conflicts:** Make sure required ports (8000, 8001, 11434, 3000) are free.
- **Ngrok not working:** Verify your firewall and use the correct port.

---

## 📄 License

MIT License. See [LICENSE](LICENSE).

---

## 🤝 Contributing

Pull requests and issues are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) if available.

---
