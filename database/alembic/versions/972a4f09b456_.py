"""empty message

Revision ID: 972a4f09b456
Revises: a890ff05d489
Create Date: 2020-06-19 18:10:21.218838

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '972a4f09b456'
down_revision = 'a890ff05d489'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assessments', sa.Column('user_id', postgresql.UUID(), nullable=True, comment='ID пользователя.'))
    op.create_index(op.f('ix_assessments_user_id'), 'assessments', ['user_id'], unique=False)
    op.create_foreign_key(None, 'assessments', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'assessments', type_='foreignkey')
    op.drop_index(op.f('ix_assessments_user_id'), table_name='assessments')
    op.drop_column('assessments', 'user_id')
    # ### end Alembic commands ###