"""Initial migration

Revision ID: 001
Revises:
Create Date: 2026-04-25

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('google_sub', sa.String(255), nullable=False, unique=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('picture', sa.String(512), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_login', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    )

    op.create_table(
        'projects',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    )

    op.create_table(
        'project_members',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    )

    op.create_table(
        'secrets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('encrypted_value', sa.Text(), nullable=False),
        sa.Column('encryption_key', sa.String(64), nullable=False),
        sa.Column('project_id', sa.Integer(), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('reads_remaining', sa.Integer(), server_default='-1', nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
    )

    op.create_table(
        'member_secret_access',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('project_member_id', sa.Integer(), sa.ForeignKey('project_members.id', ondelete='CASCADE'), nullable=False),
        sa.Column('secret_id', sa.Integer(), sa.ForeignKey('secrets.id', ondelete='CASCADE'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('member_secret_access')
    op.drop_table('secrets')
    op.drop_table('project_members')
    op.drop_table('projects')
    op.drop_table('users')