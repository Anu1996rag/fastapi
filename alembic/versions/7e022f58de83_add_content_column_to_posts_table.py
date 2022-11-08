"""add content column to posts table

Revision ID: 7e022f58de83
Revises: 6b30b6f8eb8f
Create Date: 2022-11-08 14:46:45.616282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e022f58de83'
down_revision = '6b30b6f8eb8f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', column=sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', column_name='content')
    pass
