"""modificando tipo da row user_id na yabela session

Revision ID: 802eed544462
Revises: 1e7af904f9d3
Create Date: 2024-02-18 01:02:16.249934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '802eed544462'
down_revision = '1e7af904f9d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('session', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###
