"""Baseline existing schema

Revision ID: d96a7d68518d
Revises: 
Create Date: 2025-06-20 12:27:48.860622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd96a7d68518d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    pass

def downgrade():
    pass
