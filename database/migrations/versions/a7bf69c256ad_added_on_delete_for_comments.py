"""Added on delete for comments

Revision ID: a7bf69c256ad
Revises: 2bb8bb72a38f
Create Date: 2022-05-04 17:14:18.611168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7bf69c256ad'
down_revision = '2bb8bb72a38f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comments_parent_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'comments', ['parent_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_parent_id_fkey', 'comments', 'comments', ['parent_id'], ['id'])
    # ### end Alembic commands ###
