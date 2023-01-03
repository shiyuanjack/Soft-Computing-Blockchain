"""empty message

Revision ID: dfa8199b17b1
Revises: 
Create Date: 2022-04-08 22:45:08.648527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfa8199b17b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_table',
    sa.Column('ADMIN_ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ADMIN_NAME', sa.String(length=15), nullable=False),
    sa.Column('ADMIN_PASSWORD', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('ADMIN_ID')
    )
    op.create_table('node_table',
    sa.Column('NODE_ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('NODE_NAME', sa.String(length=15), nullable=False),
    sa.Column('NODE_IP', sa.String(length=128), nullable=False),
    sa.Column('NODE_TYPE', sa.String(length=15), nullable=False),
    sa.Column('NODE_NOTE', sa.String(length=15), nullable=True),
    sa.Column('NODE_STATE', sa.String(length=128), nullable=False),
    sa.Column('NODE_TIME', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('NODE_ID')
    )
    op.create_table('user_table',
    sa.Column('USER_ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('USER_NAME', sa.String(length=15), nullable=False),
    sa.Column('USER_PASSWORD', sa.String(length=128), nullable=False),
    sa.Column('USER_EAMIL', sa.String(length=15), nullable=False),
    sa.Column('USER_PHONE', sa.String(length=15), nullable=False),
    sa.Column('USER_DES', sa.String(length=128), nullable=False),
    sa.Column('USER_RSAPK', sa.String(length=1000), nullable=False),
    sa.Column('USER_RSASK', sa.String(length=2500), nullable=False),
    sa.Column('USER_PERMIT', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('USER_ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_table')
    op.drop_table('node_table')
    op.drop_table('admin_table')
    # ### end Alembic commands ###
