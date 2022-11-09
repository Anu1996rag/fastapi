"""add content column to posts table

Revision ID: 17849fbd7e9c
Revises: bb3bfc72e150
Create Date: 2022-11-09 16:59:24.626104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17849fbd7e9c'
down_revision = 'bb3bfc72e150'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
