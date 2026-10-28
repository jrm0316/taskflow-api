"""add priority check constraint

Revision ID: cd47568e23d4
Revises: 67f8bcda4699
Create Date: 2026-09-30 17:54:46.696569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd47568e23d4'
down_revision: Union[str, Sequence[str], None] = '67f8bcda4699'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "ck_tasks_priority_range",
        "tasks",
        "priority >= 0 AND priority <= 2"
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_tasks_priority_range",
        "tasks",
        type_="check"
    )
