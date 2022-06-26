"""Added year_founded to Company11

Revision ID: 3bb1c82b8309
Revises: f9f9b191450f
Create Date: 2022-06-25 20:18:35.451650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bb1c82b8309'
down_revision = 'f9f9b191450f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('is_group', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'is_group')
    # ### end Alembic commands ###