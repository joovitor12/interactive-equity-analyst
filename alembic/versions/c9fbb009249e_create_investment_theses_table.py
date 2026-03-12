"""create investment_theses table

Revision ID: c9fbb009249e
Revises: 
Create Date: 2026-03-12 09:30:31.228282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = 'c9fbb009249e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('investment_theses',
          sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
          sa.Column('ticker', sa.String(10), nullable=False),
          sa.Column('thesis_type', sa.String(10), nullable=False),  # 'bull' or 'bear'
          sa.Column('content', sa.Text(), nullable=False),
          sa.Column('price_at_creation', sa.Float(), nullable=True),
          sa.Column('target_price', sa.Float(), nullable=True),
          sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
      )
    op.create_index('ix_investment_theses_ticker', 'investment_theses', ['ticker'])


def downgrade() -> None:
    op.drop_index('ix_investment_theses_ticker')
    op.drop_table('investment_theses')
