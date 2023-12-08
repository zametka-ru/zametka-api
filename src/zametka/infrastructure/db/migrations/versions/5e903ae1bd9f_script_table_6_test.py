"""Script table 6 test

Revision ID: 5e903ae1bd9f
Revises: ff2086bf7dbe
Create Date: 2023-05-24 11:37:10.214767

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5e903ae1bd9f"
down_revision = "ff2086bf7dbe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("notes", "text")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "notes",
        sa.Column("text", sa.String(60000), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
