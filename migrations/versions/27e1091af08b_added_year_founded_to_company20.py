"""Added year_founded to Company20

Revision ID: 27e1091af08b
Revises: 3bb1c82b8309
Create Date: 2022-06-26 11:18:04.476374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27e1091af08b'
down_revision = '3bb1c82b8309'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('group', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'message', 'group', ['group'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.drop_column('message', 'group')
    # ### end Alembic commands ###