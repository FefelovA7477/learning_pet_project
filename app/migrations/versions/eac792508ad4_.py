"""empty message

Revision ID: eac792508ad4
Revises: 2da34a2835e9
Create Date: 2024-07-12 19:26:32.516187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eac792508ad4'
down_revision: Union[str, None] = '2da34a2835e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


enum_type_name = 'taskstatuschoice'
new_enum_variant = 'ACTIVE'

def upgrade():
    op.execute(f"ALTER TYPE {enum_type_name} ADD VALUE '{new_enum_variant}';")

def downgrade():
    raise NotImplementedError("Downgrade is not implemented yet for adding new enum values.")
