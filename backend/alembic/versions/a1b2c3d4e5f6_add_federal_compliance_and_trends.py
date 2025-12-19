"""Add federal compliance and health score trends

Revision ID: a1b2c3d4e5f6
Revises: d0d3398d0750
Create Date: 2025-12-18 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'd0d3398d0750'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add federal compliance fields to contracts (the differentiator!)
    Add trend tracking to health_scores
    """
    # Federal compliance fields on contracts
    op.add_column('contracts', sa.Column('economic_buyer', sa.String(), nullable=True))
    op.add_column('contracts', sa.Column('fedramp_required', sa.Boolean(), server_default='false', nullable=True))
    op.add_column('contracts', sa.Column('fisma_level', sa.String(), server_default='none', nullable=True))
    op.add_column('contracts', sa.Column('hipaa_required', sa.Boolean(), server_default='false', nullable=True))
    op.add_column('contracts', sa.Column('section_508_required', sa.Boolean(), server_default='false', nullable=True))
    op.add_column('contracts', sa.Column('ato_status', sa.String(), server_default='none', nullable=True))
    op.add_column('contracts', sa.Column('ato_expiry_date', sa.Date(), nullable=True))
    
    # Trend tracking on health_scores
    op.add_column('health_scores', sa.Column('previous_score', sa.Integer(), nullable=True))
    op.add_column('health_scores', sa.Column('score_change', sa.Integer(), nullable=True))
    op.add_column('health_scores', sa.Column('trend_direction', sa.String(), nullable=True))
    op.add_column('health_scores', sa.Column('triggered_by', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove the new columns."""
    # Remove from contracts
    op.drop_column('contracts', 'ato_expiry_date')
    op.drop_column('contracts', 'ato_status')
    op.drop_column('contracts', 'section_508_required')
    op.drop_column('contracts', 'hipaa_required')
    op.drop_column('contracts', 'fisma_level')
    op.drop_column('contracts', 'fedramp_required')
    op.drop_column('contracts', 'economic_buyer')
    
    # Remove from health_scores
    op.drop_column('health_scores', 'triggered_by')
    op.drop_column('health_scores', 'trend_direction')
    op.drop_column('health_scores', 'score_change')
    op.drop_column('health_scores', 'previous_score')
