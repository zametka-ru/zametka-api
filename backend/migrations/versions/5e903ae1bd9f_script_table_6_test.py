"""Script table 6 test

Revision ID: 5e903ae1bd9f
Revises: ff2086bf7dbe
Create Date: 2023-05-24 11:37:10.214767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e903ae1bd9f'
down_revision = 'ff2086bf7dbe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scripts', 'text')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scripts', sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###