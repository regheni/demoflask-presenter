"""empty message

Revision ID: 6efc0f616392
Revises: 
Create Date: 2022-06-08 12:58:20.680463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6efc0f616392"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("url", sa.String(255), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("movies")
