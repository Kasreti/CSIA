"""empty message

Revision ID: bb428d008d36
Revises: 5e5c7966ff02
Create Date: 2023-12-19 15:44:03.840952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb428d008d36'
down_revision = '5e5c7966ff02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lexicon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=50), nullable=False),
    sa.Column('pronunciation', sa.String(length=50), nullable=False),
    sa.Column('conscript', sa.String(length=50), nullable=False),
    sa.Column('definition', sa.String(length=255), nullable=False),
    sa.Column('partofspeech', sa.String(length=1), nullable=False),
    sa.Column('infclass', sa.String(length=10), nullable=False),
    sa.Column('wordclass', sa.String(length=1), nullable=False),
    sa.Column('notes', sa.String(), nullable=False),
    sa.Column('etymology', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('lexicon', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_lexicon_definition'), ['definition'], unique=False)
        batch_op.create_index(batch_op.f('ix_lexicon_word'), ['word'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lexicon', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_lexicon_word'))
        batch_op.drop_index(batch_op.f('ix_lexicon_definition'))

    op.drop_table('lexicon')
    # ### end Alembic commands ###
