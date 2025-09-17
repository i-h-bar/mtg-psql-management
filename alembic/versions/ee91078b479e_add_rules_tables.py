"""add_rules_tables

Revision ID: ee91078b479e
Revises: 6c6c92fc7e9b
Create Date: 2025-09-17 14:50:14.531541

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ee91078b479e"
down_revision: Union[str, Sequence[str], None] = "6c6c92fc7e9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create mtg_rules table
    op.create_table(
        "mtg_rules",
        sa.Column("rule_number", sa.VARCHAR(length=10), nullable=False),
        sa.Column("parent_rule", sa.VARCHAR(length=10), nullable=True),
        sa.Column("section_number", sa.INTEGER(), nullable=True),
        sa.Column("section_title", sa.TEXT(), nullable=True),
        sa.Column("subsection_number", sa.INTEGER(), nullable=True),
        sa.Column("subsection_title", sa.TEXT(), nullable=True),
        sa.Column("title", sa.TEXT(), nullable=True),
        sa.Column("content", sa.TEXT(), nullable=True),
        sa.Column("keywords", postgresql.ARRAY(sa.TEXT()), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("rule_number"),
    )

    # Create indexes for mtg_rules
    op.create_index("idx_section", "mtg_rules", ["section_number", "subsection_number"])
    op.create_index("idx_keywords", "mtg_rules", ["keywords"], postgresql_using="gin")
    op.create_index(
        "idx_content_search", "mtg_rules", [sa.text("to_tsvector('english', content)")], postgresql_using="gin"
    )
    op.create_index("idx_parent_rule", "mtg_rules", ["parent_rule"])

    # Create mtg_glossary table
    op.create_table(
        "mtg_glossary",
        sa.Column("term", sa.VARCHAR(length=100), nullable=False),
        sa.Column("definition", sa.TEXT(), nullable=False),
        sa.Column("see_also", postgresql.ARRAY(sa.TEXT()), nullable=True),
        sa.Column("rule_references", postgresql.ARRAY(sa.VARCHAR(length=10)), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("term"),
    )

    # Create indexes for mtg_glossary
    op.create_index(
        "idx_term_search", "mtg_glossary", [sa.text("to_tsvector('english', term)")], postgresql_using="gin"
    )
    op.create_index(
        "idx_definition_search", "mtg_glossary", [sa.text("to_tsvector('english', definition)")], postgresql_using="gin"
    )
    op.create_index("idx_rule_references", "mtg_glossary", ["rule_references"], postgresql_using="gin")


def downgrade() -> None:
    # Drop indexes first
    op.drop_index("idx_rule_references", table_name="mtg_glossary")
    op.drop_index("idx_definition_search", table_name="mtg_glossary")
    op.drop_index("idx_term_search", table_name="mtg_glossary")

    op.drop_index("idx_parent_rule", table_name="mtg_rules")
    op.drop_index("idx_content_search", table_name="mtg_rules")
    op.drop_index("idx_keywords", table_name="mtg_rules")
    op.drop_index("idx_section", table_name="mtg_rules")

    # Drop tables
    op.drop_table("mtg_glossary")
    op.drop_table("mtg_rules")
