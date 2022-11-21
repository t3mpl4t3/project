"""Added post table

Revision ID: 130c06cd37d7
Revises: 
Create Date: 2022-11-20 21:55:42.511264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '130c06cd37d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    # ### end Alembic commands ###
