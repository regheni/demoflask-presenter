"""empty message

Revision ID: 0164afc2d1fa
Revises: 6efc0f616392
Create Date: 2022-06-08 13:50:35.143210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0164afc2d1fa"
down_revision = "6efc0f616392"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("movies", sa.Column("release_year", sa.Integer()))


def downgrade() -> None:
    pass
