"""fix_update_onupdate_default

Revision ID: 0720aedb9093
Revises: b86ff46aa9e5
Create Date: 2025-06-27 19:33:28.440574

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '0720aedb9093'
down_revision: Union[str, Sequence[str], None] = 'b86ff46aa9e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	"""Upgrade schema."""
	# ### commands auto generated by Alembic - please adjust! ###
	pass
	# ### end Alembic commands ###


def downgrade() -> None:
	"""Downgrade schema."""
	# ### commands auto generated by Alembic - please adjust! ###
	pass
	# ### end Alembic commands ###
