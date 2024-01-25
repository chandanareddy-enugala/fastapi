"""add new column to post table

Revision ID: c57fcafa98bf
Revises: 557b231e7eac
Create Date: 2024-01-24 17:52:48.447965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c57fcafa98bf'
down_revision: Union[str, None] = '557b231e7eac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
