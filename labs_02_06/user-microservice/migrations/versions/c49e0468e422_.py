"""empty message

Revision ID: c49e0468e422
Revises: 
Create Date: 2024-05-30 18:11:21.946239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# идентификаторы, используемые Alembic
revision: str = 'c49e0468e422'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Команды генерируемые Alembic 
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(length=200), nullable=False),
    sa.Column('username', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('registered_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)


def downgrade() -> None:
    # Команды генерируемые Alembic 
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
