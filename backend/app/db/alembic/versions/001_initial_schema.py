"""Initial schema creation

Revision ID: 001
Revises: 
Create Date: 2025-10-31 23:39:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade - create tables."""
    pass  # Tables already created


def downgrade() -> None:
    """Downgrade - drop tables."""
    pass
