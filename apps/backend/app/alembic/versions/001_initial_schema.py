"""initial_schema

Revision ID: 001
Revises:
Create Date: 2026-06-17
"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="viewer"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(50), nullable=False),
        sa.Column("resource_id", sa.String(50), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])

    op.create_table(
        "campaigns",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("goal", sa.Text(), nullable=True),
        sa.Column("target_audience", sa.Text(), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="draft"),
        sa.Column("state_data", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("research", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("strategy", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("content_plan", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("analytics", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("learnings", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_campaigns_client_id", "campaigns", ["client_id"])

    op.create_table(
        "content_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.Column("platform", sa.String(50), nullable=False),
        sa.Column("content_type", sa.String(50), nullable=False),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("asset_urls", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("status", sa.String(50), nullable=False, server_default="draft"),
        sa.Column("brand_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("quality_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("is_rejected", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("publish_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("platform_post_id", sa.String(255), nullable=True),
        sa.Column("views", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("likes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("shares", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("comments_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_content_items_campaign_id", "content_items", ["campaign_id"])


def downgrade() -> None:
    op.drop_table("content_items")
    op.drop_table("campaigns")
    op.drop_table("audit_logs")
    op.drop_table("users")
