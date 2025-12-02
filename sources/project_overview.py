import logging
from functools import wraps

import pandas as pd
from bs4 import BeautifulSoup
from lark import Tree as LarkTree, Token as LarkToken, logger

from sources.parsers.rockwell import l5x_parser


def _routine_explorer(soup: BeautifulSoup, *args, **kwargs):
    total_routines = len(soup.css.select("Program Routine"))
    visited_routines = 0

    programs = soup.find_all("Program")
    for program in programs:
        program_name = program.attrs["Name"]
        logging.debug(f"Visiting program {program_name}")

        routines = program.find_all("Routine")
        for routine in routines:
            routine_name = routine.attrs["Name"]
            logging.debug(f"Visiting routine {routine_name}")

            routine_plain = ""

            rungs = routine.find_all("Rung")
            for i, rung in enumerate(rungs):
                logging.debug(f"Collecting rung {i}")

                text = rung.find("Text")
                if text is not None:
                    routine_plain += text.text

            routine_plain = routine_plain.strip()

            if routine_plain:
                logging.debug(f"Parsing routine {routine_name}")

                try:
                    routine_parsed: LarkTree = l5x_parser.parse(routine_plain)
                except Exception:
                    logging.warning(
                        f"Parser error occured. Routine {routine_name} skipped"
                    )
                    continue
                yield program_name, routine_name, routine_parsed
            else:
                logging.debug(f"Routine {routine_name} is empty, skipped")


def explore_basic_statistics(project_xml: BeautifulSoup) -> pd.DataFrame:
    stat_rows = []
    for program_name, routine_name, routine_parsed in _routine_explorer(project_xml):
        for i, rung_parsed in enumerate(routine_parsed.children):
            row = {
                "program_name": program_name,
                "routine_name": routine_name,
                "rung_index": i,
                "stat_rung_instructions": 0,
                "stat_rung_tags": 0,
            }

            for subtree in rung_parsed.iter_subtrees():
                if subtree.data == "instruction":
                    row["stat_rung_instructions"] += 1
                    opcode = subtree.children[0].value  # type: ignore
                    try:
                        row[opcode] += 1
                    except KeyError:
                        row[opcode] = 1
                    for token in subtree.iter_subtrees():
                        if token.data == "tag_reference":
                            row["stat_rung_tags"] += 1

            logging.info(row)
            stat_rows.append(row)

    return pd.DataFrame(stat_rows)
