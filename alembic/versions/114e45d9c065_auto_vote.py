"""auto vote

Revision ID: 114e45d9c065
Revises: 3f5393486a1f
Create Date: 2022-11-08 15:14:18.681192

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '114e45d9c065'
down_revision = '3f5393486a1f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(('post_id',), ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(('user_id',), ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
