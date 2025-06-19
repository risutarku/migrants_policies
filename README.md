# 🚀 Quick Docker Setup for Policy Issue

Spin‑up** ****backend** (FastAPI) and** ****frontend** (Vue + Nginx) with a single command.

---

## Prerequisites

| Tool           | Version      | Check                      |
| -------------- | ------------ | -------------------------- |
| Docker Engine  | 20.10 +      | `docker -v`              |
| Docker Compose | v2 (≥ 1.29) | `docker compose version` |

> **No local Python/Node needed.** Everything runs in containers.

---

## 1 · Clone the repo

```bash
git clone https://github.com/your-org/policy-issue.git
cd policy-issue
```

---

<h2> 2 · Build & up (one‑liner)

```bash
# from repo root
docker compose up -d --build
```

*First run* builds Node/Poetry layers (~3–4 min). Subsequent** **`up` is instant.

---

## 3· Open your browser

| Service  | URL                                                   |
| -------- | ----------------------------------------------------- |
| Frontend | [http://localhost:8080](http://localhost:8080/)          |
| API docs | [http://localhost:8000/docs](http://localhost:8000/docs) |

> **Tip :** add** **`127.0.0.1 policy.local` in** **`/etc/hosts` and open** **[http://policy.local:8080](http://policy.local:8080/).

---

## 4· Logs & rebuild

```bash
# live logs (all services)
docker compose logs -f

# restart just the backend after code edits
docker compose up -d --build backend
```

---

## 5· Shut down

```bash
docker compose down        # stop & remove containers★
```

★ Volumes** **`./data` are** ****not** removed — CSV/scan files persist.

---

## Directory Map (⊶ 90 %)

```
backend/        FastAPI app, Dockerfile
frontend_app/   Vue + Vite SPA, Dockerfile
data/           CSV exports, scans
```

---

## Troubleshooting

| Symptom                     | Fix                                                                              |
| --------------------------- | -------------------------------------------------------------------------------- |
| `CORS Missing Allow-Origin` | Frontend env `VITE_API_URL=http://backend:8000` must match compose service name. |
| Port already in use         | Change `ports:` in compose or stop conflicting service (`lsof -i :8080`).        |
| Build slow every time       | Ensure `.dockerignore` lists `node_modules`, `__pycache__`, `tests`, etc.        |

---

MIT © 2025 – Demo project for Ingosstrakh. Not production‑hardened.

