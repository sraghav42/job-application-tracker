"""Added req_id to job_applications

Revision ID: 89f1d78aa886
Revises: afd7adfb197f
Create Date: 2025-02-09 17:18:33.661294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89f1d78aa886'
down_revision: Union[str, None] = 'afd7adfb197f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_applications', sa.Column('req_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job_applications', 'req_id')
    # ### end Alembic commands ###
