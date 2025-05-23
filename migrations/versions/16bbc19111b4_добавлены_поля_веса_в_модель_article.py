"""Добавлены поля веса в модель Article

Revision ID: 16bbc19111b4
Revises: e5499c614192
Create Date: 2025-05-23 22:11:37.022634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16bbc19111b4'
down_revision = 'e5499c614192'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weight_real', sa.Float(precision=5), nullable=False, server_default="0.0"))
        batch_op.add_column(sa.Column('weight_code', sa.Float(precision=1), nullable=False, server_default="0.0"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('weight_code')
        batch_op.drop_column('weight_real')

    # ### end Alembic commands ###
