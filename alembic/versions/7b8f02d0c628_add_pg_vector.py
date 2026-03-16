"""add pg_vector

Revision ID: 7b8f02d0c628
Revises: c9fbb009249e
Create Date: 2026-03-16 20:57:50.220256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b8f02d0c628'
down_revision: Union[str, Sequence[str], None] = 'c9fbb009249e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP EXTENSION IF EXISTS vector")
