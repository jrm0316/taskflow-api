"""initial migration

Revision ID: 95f9d9deadb6
Revises: 
Create Date: 2026-09-28 17:10:12.532111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95f9d9deadb6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
    )    

def downgrade() -> None:
    op.drop_table("tasks")
