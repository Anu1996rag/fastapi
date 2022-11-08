"""create posts table

Revision ID: 6b30b6f8eb8f
Revises: 
Create Date: 2022-11-08 14:34:18.399489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b30b6f8eb8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
    pass
