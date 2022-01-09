"""empty message

Revision ID: ac22a9d0c062
Revises: 52affdb6d0d9
Create Date: 2022-01-09 02:52:12.435168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac22a9d0c062'
down_revision = '52affdb6d0d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('zip_code', sa.String(length=10), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'zip_code')
    # ### end Alembic commands ###
