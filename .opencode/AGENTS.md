# AI Marketing OS — Project Context

## Stack
- Backend: FastAPI + LangGraph + Celery + SQLAlchemy (async) + PostgreSQL + Redis
- Frontend: Vue 3 + Nuxt 3 + TailwindCSS + ECharts
- Video: Remotion (server-side, Celery workers)
- LLM: NVIDIA API (deepseek-ai/deepseek-v4-pro, qwen/qwen-image, resemble-ai/chatterbox-multilingual-tts)
- Video Gen: ComfyUI (Wan2.2/LTX/Hunyuan — GPU needed)
- Publishing: SocialClaw (6 platforms)
- Storage: Cloudflare R2 (S3-compatible)
- Deployment: Railway (MVP), Docker

## Repo Structure
```
/
├── apps/
│   ├── backend/        # FastAPI app (Python)
│   │   ├── app/
│   │   │   ├── agents/       # LangGraph agent definitions
│   │   │   ├── api/v1/       # REST API routes
│   │   │   ├── config/       # Pydantic settings
│   │   │   ├── core/         # DB, security, base classes
│   │   │   ├── models/       # SQLAlchemy ORM models
│   │   │   ├── schemas/      # Pydantic request/response schemas
│   │   │   ├── services/     # Business logic
│   │   │   ├── tasks/        # Celery task definitions
│   │   │   └── workers/      # Celery app config
│   │   └── tests/
│   ├── frontend/       # Nuxt 3 app (Vue)
│   └── remotion/       # Remotion video editor (React)
├── packages/
│   ├── agent-core/     # Shared agent base classes (Python)
│   ├── llm-client/     # NVIDIA API client (Python)
│   └── shared-types/   # Shared Pydantic models (Python)
├── .env.example
├── pnpm-workspace.yaml
└── Project.md
```

## Key Conventions
- Async everywhere (FastAPI async handlers, asyncpg, async SQLAlchemy)
- JWT auth with RBAC (admin, manager, content_reviewer, viewer)
- Approval queue: all content must be human-approved before publishing
- Sequential LangGraph edges (one agent after another via PostgreSQL checkpointer)
- Celery for async tasks (Remotion renders, publishing)
- pip install -e . for all Python packages during dev
- pnpm for JS/TS packages
