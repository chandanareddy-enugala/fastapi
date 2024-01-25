"""add user tabel

Revision ID: 9cf587bd9ba4
Revises: c57fcafa98bf
Create Date: 2024-01-24 18:17:04.941181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cf587bd9ba4'
down_revision: Union[str, None] = 'c57fcafa98bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable=False),
                     sa.Column('email',sa.String(),nullable=False) ,
                     sa.Column('password',sa.String(),nullable=False),
                     sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                               server_default=sa.text('now()'),nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
