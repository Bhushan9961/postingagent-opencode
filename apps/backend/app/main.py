from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.campaigns import router as campaigns_router
from app.api.v1.content import router as content_router
from app.config.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.app_debug,
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
    return {"status": "ok", "app": settings.app_name, "version": settings.app_version}
