"""Script table 7 test

Revision ID: 6a2ab4ef3b89
Revises: 5e903ae1bd9f
Create Date: 2023-05-24 11:38:30.813533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a2ab4ef3b89'
down_revision = '5e903ae1bd9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scripts', sa.Column('text', sa.Text(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scripts', 'text')
    # ### end Alembic commands ###