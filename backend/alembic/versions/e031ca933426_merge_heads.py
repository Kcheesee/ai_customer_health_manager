"""merge_heads

Revision ID: e031ca933426
Revises: 353f9e4b8ea0, a1b2c3d4e5f6
Create Date: 2025-12-19 17:43:32.299841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e031ca933426'
down_revision: Union[str, Sequence[str], None] = ('353f9e4b8ea0', 'a1b2c3d4e5f6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
