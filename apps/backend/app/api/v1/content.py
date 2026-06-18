from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import Role, get_current_user, require_role
from app.models.content import Content, ContentStatus
from app.models.user import User
from app.schemas.content import ContentApproval, ContentRead

router = APIRouter(prefix="/content", tags=["content"])


@router.get("/pending", response_model=list[ContentRead])
async def list_pending(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Content).where(Content.status == ContentStatus.APPROVAL_PENDING)
    )
    return result.scalars().all()


@router.post("/{content_id}/approve", response_model=ContentRead)
async def approve_content(
    content_id: int,
    payload: ContentApproval,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(Role.REVIEWER)),
):
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if payload.approved:
        content.status = ContentStatus.APPROVED
        content.is_rejected = False
    else:
        content.status = ContentStatus.REJECTED
        content.is_rejected = True
        content.rejection_reason = payload.rejection_reason
    await db.commit()
    await db.refresh(content)
    return content
