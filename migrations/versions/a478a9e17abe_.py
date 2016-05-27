"""empty message

Revision ID: a478a9e17abe
Revises: e421004ed0e5
Create Date: 2016-05-26 21:24:52.019944

"""

# revision identifiers, used by Alembic.
revision = 'a478a9e17abe'
down_revision = 'e421004ed0e5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('name', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chats', 'name')
    ### end Alembic commands ###
