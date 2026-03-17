"""create analyst_opinions table

Revision ID: 902be71484b8
Revises: 7b8f02d0c628
Create Date: 2026-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '902be71484b8'
down_revision: Union[str, None] = '7b8f02d0c628'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'analyst_opinions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('ticker', sa.String(10), nullable=False),
        sa.Column('source', sa.String(100), nullable=False),  # e.g., "Investing.com", "Goldman Sachs"
        sa.Column('rating', sa.String(50), nullable=True),     # e.g., "Buy", "Hold", "Sell"
        sa.Column('price_target', sa.Float(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),        # Key points from the opinion
        sa.Column('raw_content', sa.Text(), nullable=True),    # Full scraped content
        sa.Column('scraped_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('ix_analyst_opinions_ticker', 'analyst_opinions', ['ticker'])


def downgrade() -> None:
    op.drop_index('ix_analyst_opinions_ticker')
    op.drop_table('analyst_opinions')
