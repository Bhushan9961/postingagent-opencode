from dataclasses import dataclass
from typing import Any

import httpx

from app.config.config import settings


@dataclass
class PostResult:
    platform: str
    status: str
    post_id: str | None = None
    url: str | None = None
    error: str | None = None


class LinkedInClient:
    BASE_URL = "https://api.linkedin.com"

    def __init__(self, access_token: str = "", author_urn: str = ""):
        self.access_token = access_token or settings.linkedin_access_token
        self.author_urn = author_urn or settings.linkedin_author_urn
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0",
                },
                timeout=30.0,
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def create_post(self, text: str, image_url: str | None = None) -> PostResult:
        if not self.access_token or not self.author_urn:
            return PostResult(platform="linkedin", status="skipped", error="tokens not configured")

        client = await self._get_client()
        body: dict[str, Any] = {
            "author": self.author_urn,
            "commentary": text,
            "visibility": "PUBLIC",
        }

        if image_url:
            body["content"] = {
                "media": {"title": "", "id": await self._upload_image(image_url)}
            }
        else:
            body["lifecycleState"] = "PUBLISHED"

        r = await client.post("/rest/posts", json=body)
        if r.status_code not in (200, 201):
            return PostResult(platform="linkedin", status="failed", error=r.text)

        post_id = r.json().get("id", "")
        return PostResult(
            platform="linkedin",
            status="published",
            post_id=post_id,
            url=f"https://linkedin.com/feed/update/{post_id}",
        )

    async def _upload_image(self, image_url: str) -> str:
        return ""


class FacebookClient:
    BASE_URL = "https://graph.facebook.com/v22.0"

    def __init__(self, page_access_token: str = "", page_id: str = ""):
        self.page_access_token = page_access_token or settings.facebook_page_access_token
        self.page_id = page_id or settings.facebook_page_id
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=self.BASE_URL, timeout=30.0)
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def create_post(self, text: str, image_url: str | None = None) -> PostResult:
        if not self.page_access_token or not self.page_id:
            return PostResult(platform="facebook", status="skipped", error="tokens not configured")

        client = await self._get_client()
        params = {"access_token": self.page_access_token, "message": text}

        if image_url:
            r = await client.post(f"/{self.page_id}/photos", params={**params, "url": image_url})
        else:
            r = await client.post(f"/{self.page_id}/feed", params=params)

        if r.status_code not in (200, 201):
            return PostResult(platform="facebook", status="failed", error=r.text)

        data = r.json()
        post_id = data.get("id", "")
        return PostResult(
            platform="facebook", status="published", post_id=post_id
        )


class InstagramClient:
    BASE_URL = "https://graph.facebook.com/v22.0"

    def __init__(self, page_access_token: str = "", business_account_id: str = ""):
        self.page_access_token = page_access_token or settings.facebook_page_access_token
        self.business_account_id = business_account_id or settings.instagram_business_account_id
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=self.BASE_URL, timeout=30.0)
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def create_post(self, text: str, image_url: str | None = None) -> PostResult:
        if not self.page_access_token or not self.business_account_id:
            return PostResult(platform="instagram", status="skipped", error="tokens not configured")

        client = await self._get_client()
        params = {"access_token": self.page_access_token}

        if image_url:
            create = await client.post(
                f"/{self.business_account_id}/media",
                params={**params, "image_url": image_url, "caption": text},
            )
        else:
            create = await client.post(
                f"/{self.business_account_id}/media",
                params={**params, "image_url": "", "caption": text},
            )

        if create.status_code not in (200, 201):
            return PostResult(platform="instagram", status="failed", error=create.text)

        container_id = create.json().get("id", "")
        publish = await client.post(
            f"/{self.business_account_id}/media_publish",
            params={**params, "creation_id": container_id},
        )

        if publish.status_code not in (200, 201):
            return PostResult(platform="instagram", status="failed", error=publish.text)

        post_id = publish.json().get("id", "")
        return PostResult(platform="instagram", status="published", post_id=post_id)


class SocialPublisherError(Exception):
    def __init__(self, message: str, details: Any = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class SocialPublisher:
    def __init__(
        self,
        linkedin_token: str = "",
        linkedin_urn: str = "",
        facebook_token: str = "",
        facebook_page: str = "",
        ig_account: str = "",
    ):
        self.linkedin = LinkedInClient(linkedin_token, linkedin_urn)
        self.facebook = FacebookClient(facebook_token, facebook_page)
        self.instagram = InstagramClient(facebook_token or None, ig_account)

    async def close(self) -> None:
        await self.linkedin.close()
        await self.facebook.close()
        await self.instagram.close()

    async def publish(
        self, platform: str, text: str, image_url: str | None = None
    ) -> PostResult:
        match platform:
            case "linkedin":
                return await self.linkedin.create_post(text, image_url)
            case "facebook":
                return await self.facebook.create_post(text, image_url)
            case "instagram":
                return await self.instagram.create_post(text, image_url)
            case _:
                return PostResult(
                    platform=platform, status="skipped", error=f"unsupported platform: {platform}"
                )

    async def publish_batch(self, posts: list[dict]) -> list[PostResult]:
        results: list[PostResult] = []
        for post in posts:
            result = await self.publish(
                platform=post.get("platform", ""),
                text=post.get("text", ""),
                image_url=post.get("image_url"),
            )
            results.append(result)
        return results
