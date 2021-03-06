"""empty message

Revision ID: 3957a85cab2a
Revises: af190bf8a1f1
Create Date: 2019-12-27 10:30:19.222914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3957a85cab2a'
down_revision = 'af190bf8a1f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['recourses.id'], ),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###
