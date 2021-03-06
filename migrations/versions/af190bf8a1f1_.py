"""empty message

Revision ID: af190bf8a1f1
Revises: 728abaa3a6a8
Create Date: 2019-12-20 16:36:36.099285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af190bf8a1f1'
down_revision = '728abaa3a6a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('recourse_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recourse_id'], ['recourses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recomments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recomments')
    op.drop_table('comments')
    # ### end Alembic commands ###
