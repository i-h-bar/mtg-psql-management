import asyncio
import os
import re
from pathlib import Path

import aiohttp
import asyncpg
from dotenv import load_dotenv

from db.queries.tables import mtg_glossary, mtg_rules
from models.rules.definition import Definition
from models.rules.rule import Rule

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


def parse_rules(rules_content: str) -> tuple[list[Rule], list[Definition]]:
    sections = dict(SECTIONS_RE.findall(rules_content.split("Glossary")[0]))
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
            section = number[0]
            section_title = sections[section]
            subsection = number.split(".")[0]
            subsection_title = sections[subsection]
            cleaned_rules.append(
                Rule(
                    number=number,
                    parent=parent,
                    section=int(section),
                    section_title=section_title,
                    subsection=int(subsection),
                    subsection_title=subsection_title,
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

    return cleaned_rules, cleaned_glossary


async def insert_rules() -> None:
    rules = await get_rules()
    rules, glossary = parse_rules(rules)

    async with asyncpg.create_pool(dsn=os.getenv("PSQL_URI")) as pool:
        await asyncio.gather(
            *(
                pool.execute(
                    mtg_rules.INSERT,
                    rule.number,
                    rule.parent,
                    rule.section,
                    rule.section_title,
                    rule.subsection,
                    rule.subsection_title,
                    rule.content,
                )
                for rule in rules
            )
        )
        await asyncio.gather(
            *(
                pool.execute(mtg_glossary.INSERT, definition.term, definition.definition, definition.rules_reference)
                for definition in glossary
            )
        )


if __name__ == "__main__":
    asyncio.run(insert_rules())
