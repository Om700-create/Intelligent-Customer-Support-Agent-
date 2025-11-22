# Intelligent-Customer-Support-Agent-
# 🧠 Intelligent Customer Support Agent (AI-Powered, Full-Stack System)

![Project Banner](/mnt/data/A_2D_digital_graphic_design_banner_showcases_the_t.png)

An enterprise-grade **AI Customer Support Platform** built with:

- **FastAPI + PostgreSQL + SQLAlchemy + Alembic**
- **React (Vite + TypeScript) + Tailwind CSS**
- **Hugging Face Inference API**
- **JWT Authentication (agents + admins)**
- **Full conversation storage, tagging, sentiment & intent**
- **Dark Mode Admin Dashboard (Intercom/Zendesk-style)**
- **Docker + docker-compose + Nginx**
- **GitHub Actions CI/CD**

A complete modern AI-powered support solution similar to Intercom or Zendesk.

---

## 📸 UI Preview (Dark Mode)

![Customer Support Dashboard](/mnt/data/A_digital_screenshot_displays_a_professional_custo.png)

---

## 🚀 Features

### 🧠 AI-Powered Support
- Text generation: `google/gemma-2-2b-it`
- Intent classification: `facebook/bart-large-mnli`
- Sentiment analysis: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- Auto-tagging  
- Conversation memory  
- Professional system prompting  

---

### 👨‍💻 Admin / Agent Dashboard

- View all conversations  
- Status (open, assigned, resolved)  
- Intent, sentiment, confidence  
- Tags (invoice, login, refund, crash, etc.)  
- Assign agents  
- Full message history  
- Dark-mode SaaS design  

---

### 🔐 Authentication

- JWT login  
- Role-based access (admin, agent)  

---

### 🗄 PostgreSQL Database Schema

Tables:

- `users`
- `conversations`
- `messages`  
- enums: `user_role`, `conversation_status`, `message_sender_type`

Version controlled via **Alembic migrations**.

---

## 🐳 Docker Architecture

frontend (React)
backend (FastAPI)
postgres (database)
nginx (reverse proxy)

yaml
Copy code

---

## 📁 Project Structure

intelligent-support-agent/
├─ backend/
│ ├─ app/
│ │ ├─ core/
│ │ ├─ models/
│ │ ├─ services/
│ │ ├─ routers/
│ │ ├─ schemas/
│ │ └─ prompts/
│ ├─ alembic/
│ └─ Dockerfile
├─ frontend/
│ ├─ src/
│ └─ Dockerfile
├─ infra/
├─ docker-compose.yml
└─ README.md

yaml
Copy code

---

## 🏗 Installation

### 1️⃣ Clone

```bash
git clone <your-repo-url>
cd intelligent-support-agent
2️⃣ Setup environment
bash
Copy code
cp .env.example .env
Edit .env with:

HuggingFace API key

Postgres credentials

JWT secret

3️⃣ Run
bash
Copy code
docker-compose up --build
4️⃣ Access:
Frontend → http://localhost

Backend docs → http://localhost/api/docs

Health → http://localhost/health

🧪 Test Chat API
bash
Copy code
curl -X POST http://localhost/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "test-123",
    "message": "I need help with billing",
    "channel": "web"
  }'
Returns intent + sentiment + tags + AI reply.

🔄 CI/CD
Workflow path:

bash
Copy code
.github/workflows/ci.yml
Includes:

Frontend build

Backend build

Tests

Docker image push

🤝 Contributing
See: CONTRIBUTING.md

📜 License
MIT — see LICENSE

📝 Changelog
See: CHANGELOG.md