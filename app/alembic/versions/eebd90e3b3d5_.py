"""empty message

Revision ID: eebd90e3b3d5
Revises: 582b9383c708
Create Date: 2022-12-08 12:31:32.801113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eebd90e3b3d5'
down_revision = '582b9383c708'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('order', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'order')
    # ### end Alembic commands ###
