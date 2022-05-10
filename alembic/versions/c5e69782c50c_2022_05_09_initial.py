"""2022_05_09_initial

Revision ID: c5e69782c50c
Revises: 
Create Date: 2022-05-09 21:44:04.572978

"""
from alembic import op
import sqlalchemy as sa


revision = 'c5e69782c50c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('brands',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brands_name'), 'brands', ['name'], unique=False)
    op.create_table('users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('login', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discount_codes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('brand_id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_discount_codes_brand_id'), 'discount_codes', ['brand_id'], unique=False)
    op.create_index(op.f('ix_discount_codes_created'), 'discount_codes', ['created'], unique=False)
    op.create_index(op.f('ix_discount_codes_user_id'), 'discount_codes', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_discount_codes_user_id'), table_name='discount_codes')
    op.drop_index(op.f('ix_discount_codes_created'), table_name='discount_codes')
    op.drop_index(op.f('ix_discount_codes_brand_id'), table_name='discount_codes')
    op.drop_table('discount_codes')
    op.drop_table('users')
    op.drop_index(op.f('ix_brands_name'), table_name='brands')
    op.drop_table('brands')
