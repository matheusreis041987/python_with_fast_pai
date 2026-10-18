"""cria tabela contas a pagar e receber

Revision ID: 5a7986830031
Revises: 
Create Date: 2026-09-17 20:43:20.800924

"""
#USAR COMANDO python -m alembic upgrade head

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a7986830031'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('contas_a_pagar_e_receber',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=True),
    sa.Column('valor', sa.Numeric(), nullable=True),
    sa.Column('tipo', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    op.drop_table('contas_a_pagar_e_receber')
