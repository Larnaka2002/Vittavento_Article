"""Add role field to user

Revision ID: 98e7912011b9
Revises: 89f3782e68ce
Create Date: 2025-05-27 00:31:47.880508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98e7912011b9'
down_revision = '89f3782e68ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
