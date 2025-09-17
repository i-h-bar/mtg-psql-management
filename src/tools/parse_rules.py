import os
import re
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


RULE_NUMBER = re.compile(r"\d+\.\d+(?:[a-z]+)?")
RULES_RE = re.compile(r"(\d+\.\d+(?:[a-z]+|\.)?)\s(.+)")
SECTIONS_RE = re.compile(r"(\d+)\.\s(.+)")
LOWER_RE = re.compile(r"[a-z]+")


class Rule(BaseModel):
    number: str
    parent: str
    section: int
    section_title: str
    subsection: str
    subsection_title: str
    content: str


class Definition(BaseModel):
    term: str
    definition: str
    see_also: list[str]
    rules_reference: list[str]


async def parse_rules() -> None:
    rules_content = Path(os.getenv("RULES_PATH")).read_text(encoding="utf-8")
    sections = dict(SECTIONS_RE.findall(rules_content.split("Glossary")[0]))
    rules = rules_content.split("Glossary")[1]
    glossary = rules_content.split("Glossary")[-1]
    cleaned_rules = []
    _cleaned_glossary = []

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
                    subsection=subsection,
                    subsection_title=subsection_title,
                    content=content,
                )
            )

    for term in glossary.split("\n\n"):
        if term:
            title, *content = term.split("\n")
            content = " ".join(content)
            _rule_references = RULE_NUMBER.findall(content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(parse_rules())
