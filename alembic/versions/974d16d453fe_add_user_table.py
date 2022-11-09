"""add user table

Revision ID: 974d16d453fe
Revises: 17849fbd7e9c
Create Date: 2022-11-09 17:00:00.269059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '974d16d453fe'
down_revision = '17849fbd7e9c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
