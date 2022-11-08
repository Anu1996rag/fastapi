"""add foreign key to posts table

Revision ID: f3b23c3e1a2c
Revises: 16b773d8d2db
Create Date: 2022-11-08 14:56:40.942943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3b23c3e1a2c'
down_revision = '16b773d8d2db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column(table_name='posts', column_name='owner_id')
    pass
