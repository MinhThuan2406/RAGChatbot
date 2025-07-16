# RAGChatbot Troubleshooting Guide

This guide lists common issues and solutions for running and developing RAGChatbot.

---

## 1. Service Not Starting
- **Check logs:**
  ```sh
  docker compose logs -f
  ```
- **Ports in use:** Ensure ports 8000, 8001, 11434, 3000 are free.
- **.env file:** Double-check all required environment variables are set.

---

## 2. CORS Errors
- Make sure `CORS_ALLOW_ORIGIN` in `.env` matches your frontend URL.
- Restart the backend after changing CORS settings.

---

## 3. Ngrok Not Working
- Verify your Ngrok authtoken is set in `.env` or via `ngrok config add-authtoken <token>`.
- Check firewall settings.
- Use the correct port in your Ngrok command.

---

## 4. Ollama Connection Issues in Docker
- See `open-webui/TROUBLESHOOTING.md` for Docker networking tips.
- Ensure the Ollama service is running and accessible from other containers.

---

## 5. Database (ChromaDB) Issues
- Ensure ChromaDB container is running.
- Check logs for errors on port 8000.
- Remove volumes and restart if persistent errors occur:
  ```sh
  docker compose down -v
  docker compose up --build
  ```

---

## 6. UI Not Loading
- Confirm the frontend container is running.
- Try rebuilding the frontend:
  ```sh
  docker compose up --build
  ```
- Clear browser cache.

---

## 7. Ingestion Fails
- Check file formats in `data/raw_docs/`.
- Review backend logs for ingestion errors.

---

## 8. General Debugging Tips
- Use `docker compose ps` to check container status.
- Use `docker exec -it <container> /bin/bash` to get a shell inside a container.
- For Python errors, check stack traces in backend logs.

---

## 9. Getting More Help
- Review the main `README.Docker.md` and `DEVELOPER_GUIDE.md`.
- For advanced issues, consult the developer or open an issue in your project repository.
