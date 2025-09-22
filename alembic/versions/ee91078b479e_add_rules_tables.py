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
    op.create_table(
        "mtg_rule_section",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "mtg_rule_subsection",
        sa.Column("section_id", sa.INTEGER(), nullable=False),
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.ForeignKeyConstraint(["section_id"], ["mtg_rule_section.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("section_id", "id"),
    )

    op.create_table(
        "mtg_rule",
        sa.Column("rule_number", sa.VARCHAR(length=10), nullable=False),
        sa.Column("parent_rule", sa.VARCHAR(length=10), nullable=True),
        sa.Column("section_id", sa.INTEGER(), nullable=True),
        sa.Column("subsection_id", sa.INTEGER(), nullable=True),
        sa.Column("content", sa.TEXT(), nullable=True),
        sa.ForeignKeyConstraint(["section_id"], ["mtg_rule_section.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["section_id", "subsection_id"],
            ["mtg_rule_subsection.section_id", "mtg_rule_subsection.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("rule_number"),
    )

    op.create_index(
        "idx_section_title_search",
        "mtg_rule_section",
        [sa.text("to_tsvector('english', title)")],
        postgresql_using="gin",
    )

    op.create_index(
        "idx_subsection_title_search",
        "mtg_rule_subsection",
        [sa.text("to_tsvector('english', title)")],
        postgresql_using="gin",
    )

    op.create_index("idx_section", "mtg_rule", ["section_id", "subsection_id"])
    op.create_index(
        "idx_content_search", "mtg_rule", [sa.text("to_tsvector('english', content)")], postgresql_using="gin"
    )
    op.create_index("idx_parent_rule", "mtg_rule", ["parent_rule"])

    op.create_table(
        "mtg_glossary",
        sa.Column("term", sa.VARCHAR(length=100), nullable=False),
        sa.Column("definition", sa.TEXT(), nullable=False),
        sa.Column("rule_references", postgresql.ARRAY(sa.VARCHAR(length=10)), nullable=True),
        sa.PrimaryKeyConstraint("term"),
    )

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

    op.drop_index("idx_parent_rule", table_name="mtg_rule")
    op.drop_index("idx_content_search", table_name="mtg_rule")
    op.drop_index("idx_section", table_name="mtg_rule")

    op.drop_index("idx_subsection_title_search", table_name="mtg_rule_subsection")
    op.drop_index("idx_section_title_search", table_name="mtg_rule_section")

    # Drop tables (order matters due to foreign keys)
    op.drop_table("mtg_glossary")
    op.drop_table("mtg_rule")
    op.drop_table("mtg_rule_subsection")
    op.drop_table("mtg_rule_section")
