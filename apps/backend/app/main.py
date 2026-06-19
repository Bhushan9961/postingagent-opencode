from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

import app.models.audit_log  # noqa: F401
import app.models.campaign  # noqa: F401
import app.models.content  # noqa: F401
import app.models.user  # noqa: F401
from app.api.v1.auth import router as auth_router
from app.api.v1.campaigns import router as campaigns_router
from app.api.v1.content import router as content_router
from app.config.config import settings
from app.core.database import Base, engine
from app.services.llm_client import get_llm_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(campaigns_router, prefix="/api/v1")
app.include_router(content_router, prefix="/api/v1")


@app.get("/health")
async def health():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "database": db_status,
        "has_nv_api_key": bool(settings.nvidia_api_key),
        "has_supabase_url": bool(settings.supabase_url),
        "has_supabase_key": bool(settings.supabase_service_key),
        "nvidia_base_url": settings.nvidia_base_url,
    }


@app.get("/debug/nvidia")
async def debug_nvidia():
    try:
        llm = get_llm_client()
        result = await llm.chat(
            system_prompt="You are a test assistant.",
            user_prompt="Say hello in 1 word.",
            max_tokens=20,
        )
        return {"status": "ok", "result": result, "model": "deepseek-ai/deepseek-v4-pro"}
    except Exception as e:
        return {"status": "error", "error": str(e), "type": type(e).__name__}


@app.get("/debug/image")
async def debug_image():
    try:
        llm = get_llm_client()
        url = await llm.generate_image(
            prompt="A simple test image of a blue circle on white background",
            size="1024x1024",
        )
        return {"status": "ok", "url": url}
    except Exception as e:
        return {"status": "error", "error": str(e), "type": type(e).__name__}


@app.get("/debug/raw-nvidia")
async def debug_raw_nvidia():
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.nvidia_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-ai/deepseek-v4-pro",
                    "messages": [{"role": "user", "content": "Say hello in 1 word"}],
                    "max_tokens": 10,
                },
            )
            return {
                "status_code": r.status_code,
                "headers": dict(r.headers),
                "body": r.text[:500],
            }
    except Exception as e:
        return {"status": "error", "error": str(e), "type": type(e).__name__}
