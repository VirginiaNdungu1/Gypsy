"""gypsy_blogs -Update User-related Models

Revision ID: 4d3efb65aded
Revises: 4997b43f4f99
Create Date: 2017-11-04 21:20:16.818721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d3efb65aded'
down_revision = '4997b43f4f99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('label', sa.Unicode(length=255), server_default='', nullable=True))
    op.add_column('users', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('first_name', sa.Unicode(length=50), server_default='', nullable=False))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default='0', nullable=False))
    op.add_column('users', sa.Column('last_name', sa.Unicode(length=50), server_default='', nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'confirmed_at')
    op.drop_column('roles', 'label')
    # ### end Alembic commands ###
