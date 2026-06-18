from typing import Any

import httpx

from app.config.config import settings

SUPABASE_STORAGE_URL = f"{settings.supabase_url}/storage/v1"


class StorageError(Exception):
    def __init__(self, message: str, status_code: int = 500, details: Any = None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class SupabaseStorage:
    def __init__(self):
        self.bucket = settings.storage_bucket
        self.service_key = settings.supabase_service_key
        self.base_url = SUPABASE_STORAGE_URL
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            if not self.service_key:
                raise StorageError("SUPABASE_SERVICE_KEY not configured", status_code=500)
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.service_key}",
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def upload_file(self, file_path: str, object_name: str, content_type: str | None = None) -> dict[str, Any]:
        client = await self._get_client()
        with open(file_path, "rb") as f:
            headers = {"Authorization": f"Bearer {self.service_key}"}
            if content_type:
                headers["Content-Type"] = content_type
            r = await client.post(
                f"/object/{self.bucket}/{object_name}",
                content=f.read(),
                headers=headers,
            )
        if r.status_code not in (200, 201):
            raise StorageError("Upload failed", r.status_code, r.text)
        return {"path": object_name, "url": f"{self.base_url}/object/public/{self.bucket}/{object_name}"}

    async def upload_bytes(self, data: bytes, object_name: str, content_type: str = "application/octet-stream") -> dict[str, Any]:
        client = await self._get_client()
        headers = {"Authorization": f"Bearer {self.service_key}", "Content-Type": content_type}
        r = await client.post(
            f"/object/{self.bucket}/{object_name}",
            content=data,
            headers=headers,
        )
        if r.status_code not in (200, 201):
            raise StorageError("Upload failed", r.status_code, r.text)
        return {"path": object_name, "url": f"{self.base_url}/object/public/{self.bucket}/{object_name}"}

    async def delete_file(self, object_name: str) -> None:
        client = await self._get_client()
        r = await client.delete(f"/object/{self.bucket}/{object_name}")
        if r.status_code not in (200, 204):
            raise StorageError("Delete failed", r.status_code, r.text)

    async def list_files(self, prefix: str = "") -> list[dict[str, Any]]:
        client = await self._get_client()
        r = await client.post(f"/object/list/{self.bucket}", json={"prefix": prefix})
        if r.status_code != 200:
            raise StorageError("List failed", r.status_code, r.text)
        return r.json()

    def get_public_url(self, object_name: str) -> str:
        return f"{self.base_url}/object/public/{self.bucket}/{object_name}"
