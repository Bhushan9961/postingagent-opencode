from typing import Any

import httpx

from app.config.config import settings

SOCIALCLAW_BASE_URL = "https://getsocialclaw.com"


class SocialClawError(Exception):
    def __init__(self, message: str, status_code: int = 500, details: Any = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class SocialClawClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.sc_api_key
        self.base_url = SOCIALCLAW_BASE_URL
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            if not self.api_key:
                raise SocialClawError("SC_API_KEY not configured", status_code=500)
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30.0,
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def validate_key(self) -> dict[str, Any]:
        client = await self._get_client()
        r = await client.get("/v1/keys/validate")
        if r.status_code != 200:
            raise SocialClawError("Invalid SC_API_KEY", r.status_code, r.text)
        return r.json()

    async def list_accounts(self) -> list[dict[str, Any]]:
        client = await self._get_client()
        r = await client.get("/v1/accounts")
        if r.status_code != 200:
            raise SocialClawError("Failed to list accounts", r.status_code, r.text)
        data = r.json()
        return data if isinstance(data, list) else data.get("accounts", data.get("data", []))

    async def upload_asset(self, file_path: str) -> dict[str, Any]:
        client = await self._get_client()
        with open(file_path, "rb") as f:
            r = await client.post("/v1/assets/upload", files={"file": f})
        if r.status_code != 200:
            raise SocialClawError("Failed to upload asset", r.status_code, r.text)
        return r.json()

    async def validate_schedule(self, schedule: dict[str, Any]) -> dict[str, Any]:
        client = await self._get_client()
        r = await client.post("/v1/schedule/validate", json=schedule)
        if r.status_code != 200:
            raise SocialClawError("Schedule validation failed", r.status_code, r.text)
        return r.json()

    async def apply_schedule(self, schedule: dict[str, Any]) -> dict[str, Any]:
        client = await self._get_client()
        r = await client.post("/v1/schedule/apply", json=schedule)
        if r.status_code != 200:
            raise SocialClawError("Failed to apply schedule", r.status_code, r.text)
        return r.json()

    async def get_run_status(self, run_id: str) -> dict[str, Any]:
        client = await self._get_client()
        r = await client.get(f"/v1/runs/{run_id}")
        if r.status_code != 200:
            raise SocialClawError("Failed to get run status", r.status_code, r.text)
        return r.json()

    async def list_posts(self) -> list[dict[str, Any]]:
        client = await self._get_client()
        r = await client.get("/v1/posts")
        if r.status_code != 200:
            raise SocialClawError("Failed to list posts", r.status_code, r.text)
        data = r.json()
        return data if isinstance(data, list) else data.get("posts", data.get("data", []))


PROVIDER_MAP = {
    "x": "x",
    "twitter": "x",
    "linkedin": "linkedin",
    "linkedin_page": "linkedin_page",
    "instagram": "instagram",
    "instagram_business": "instagram_business",
    "facebook": "facebook",
    "tiktok": "tiktok",
    "youtube": "youtube",
    "pinterest": "pinterest",
    "reddit": "reddit",
}

ACCOUNT_PLATFORM_MAP = {
    "x": "x",
    "linkedin": "linkedin",
    "instagram": "instagram",
    "facebook": "facebook",
    "tiktok": "tiktok",
    "youtube": "youtube",
    "pinterest": "pinterest",
}
