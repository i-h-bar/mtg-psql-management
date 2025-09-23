import asyncio
import os
import re
from pathlib import Path

import aiohttp
import asyncpg
from dotenv import load_dotenv

from db.queries.tables import mtg_glossary, mtg_rules, mtg_section, mtg_subsection
from models.rules.definition import Definition
from models.rules.rule import Rule
from models.rules.section import Section
from models.rules.subsection import SubSection

load_dotenv()


RULE_NUMBER = re.compile(r"\d+(?:\.\d+(?:[a-z]+)?)?")
SEE_SPLIT = re.compile(r"[Ss]ee\s")
RULES_RE = re.compile(r"(\d+\.\d+(?:[a-z]+|\.)?)\s(.+)")
SECTIONS_RE = re.compile(r"(\d+)\.\s(.+)")
LOWER_RE = re.compile(r"[a-z]+")


async def get_rules() -> str:
    if not (path := os.getenv("RULES_PATH")):
        return await _request_rules()

    return Path(path).read_text(encoding="utf-8")


async def _request_rules() -> str:
    async with aiohttp.ClientSession() as session:
        response = await session.get(os.getenv("RULES_URL"))
        return await response.text()


def parse_rules(rules_content: str) -> tuple[list[Rule], list[Definition], list[Section], list[SubSection]]:
    sections = dict(SECTIONS_RE.findall(rules_content.split("Glossary")[0]))

    sections_to_insert = [
        Section(id=int(section_id), title=value) for section_id, value in sections.items() if int(section_id) < 100
    ]
    subsections = [
        SubSection(id=int(section_id), section_id=int(section_id[0]), title=value)
        for section_id, value in sections.items()
        if int(section_id) >= 100
    ]

    rules = rules_content.split("Glossary")[1]
    glossary = rules_content.split("Glossary")[-1].split("Credits")[0]
    cleaned_rules = []
    cleaned_glossary = []

    for rule in rules.split("\n\n"):
        if rule and (groups := RULES_RE.search(rule)):
            number, content = groups.groups()
            content.replace("\n", " ")
            number = number.rstrip(".")
            parent = LOWER_RE.sub("", number)
            subsection = number.split(".")[0]
            cleaned_rules.append(
                Rule(
                    number=number,
                    parent=parent,
                    subsection_id=int(subsection),
                    content=content,
                )
            )

    for term in glossary.split("\n\n"):
        if term:
            title, *content = term.split("\n")
            content = " ".join(content)
            rule_references = []
            if content_split := SEE_SPLIT.split(content)[-1]:
                rule_references = RULE_NUMBER.findall(content_split)

            cleaned_glossary.append(
                Definition(
                    term=title,
                    definition=content,
                    rules_reference=rule_references,
                )
            )

    return cleaned_rules, cleaned_glossary, sections_to_insert, subsections


async def insert_rules() -> None:
    rules = await get_rules()
    rules, glossary, sections, subsections = parse_rules(rules)

    async with asyncpg.create_pool(dsn=os.getenv("PSQL_URI")) as pool:
        await asyncio.gather(
            *(
                pool.execute(
                    mtg_section.UPSERT,
                    s.id,
                    s.title,
                )
                for s in sections
            )
        )

        await asyncio.gather(
            *(
                pool.execute(
                    mtg_subsection.UPSERT,
                    s.id,
                    s.section_id,
                    s.title,
                )
                for s in subsections
            )
        )

        await asyncio.gather(
            *(
                pool.execute(
                    mtg_rules.UPSERT,
                    rule.number,
                    rule.parent,
                    rule.subsection_id,
                    rule.content,
                )
                for rule in rules
            )
        )
        await asyncio.gather(
            *(
                pool.execute(mtg_glossary.UPSERT, definition.term, definition.definition, definition.rules_reference)
                for definition in glossary
            )
        )


if __name__ == "__main__":
    asyncio.run(insert_rules())
