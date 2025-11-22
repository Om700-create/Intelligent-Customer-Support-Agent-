# Intelligent-Customer-Support-Agent-
# Intelligent Customer Support Agent (Pro Edition)

A production-style **AI Customer Support Platform** with:

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT Auth
- **AI**: Hugging Face Inference API (text generation + classification)
- **Frontend**: React (Vite + TypeScript) + Tailwind CSS
- **Database**: PostgreSQL (conversations, messages, users, roles)
- **Admin / Agent Dashboard**: Web UI
- **CI/CD**: GitHub Actions + Docker
- **Infra**: Docker Compose + Nginx reverse proxy

## Quick Start

### 1. Clone + Env

```bash
git clone <your-repo-url> intelligent-support-agent
cd intelligent-support-agent
cp .env.example .env
