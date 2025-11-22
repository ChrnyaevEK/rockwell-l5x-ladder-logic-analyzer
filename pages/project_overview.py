import os
import logging

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup, Tag
from lark import Tree as LarkTree, Token as LarkToken

import configs
from sources.parser import rockwell_l5x_parser

current_project_file_name = st.session_state[configs.SESSION_CURRENT_PROJECT_ENUM]
if current_project_file_name is None:
    st.warning("No project loaded. Go to main page and hit that load button!")
    st.stop()

current_project_file_path = st.session_state[configs.SESSION_RELATED_PROJECTS_ENUM].get(
    current_project_file_name
)
if current_project_file_path is None or not os.path.exists(current_project_file_path):
    st.warning(
        "Invalid project selected. Source files were not found. Uplaod project again."
    )
    st.stop()


@st.cache_resource
def _load_project(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, features="xml")
    except Exception as e:
        st.exception(e)
        st.stop()
    return soup


@st.cache_resource
def _parse_plain_routine(routine_plain: str):
    return rockwell_l5x_parser.parse(routine_plain)


def _build_basic_stat_df(soup: BeautifulSoup) -> pd.DataFrame:
    total = len(soup.css.select("Program Routine"))
    processed = 0

    def _update_progress():
        progress.progress(processed / total)

    rows = []
    programs = soup.find_all("Program")
    for program in programs:
        program_name = program.attrs["Name"]
        routines = program.find_all("Routine")
        for routine in routines:
            routine_name = routine.attrs["Name"]
            rungs = routine.find_all("Rung")

            routine_plain = ""
            for rung in rungs:
                tag = rung.find("Text")
                if tag is not None:
                    routine_plain += tag.text
            routine_plain = routine_plain.strip()

            if routine_plain:
                try:
                    parsed_routine: LarkTree = _parse_plain_routine(routine_plain)
                except Exception:
                    with error_log:
                        st.markdown("! Parser error occured (routine skipped).")
                        st.markdown(routine_plain)
                    continue

                for i, parsed_rung in enumerate(parsed_routine.children):
                    row = {
                        "program_name": program_name,
                        "routine_name": routine_name,
                        "rung_index": str(i),
                        "total_instructions": 0,
                        "total_tags": 0,
                    }
                    for tree in parsed_rung.iter_subtrees():
                        if tree.data == "instruction":
                            row["total_instructions"] += 1
                            opcode = tree.children[0].value  # type: ignore
                            try:
                                row[opcode] += 1
                            except KeyError:
                                row[opcode] = 1
                            for token in tree.iter_subtrees():
                                if token.data == "tag_reference":
                                    row["total_tags"] += 1
                    rows.append(row)

            processed += 1
            _update_progress()

    return pd.DataFrame(rows)


# Load XML
soup = _load_project(current_project_file_path)
st.markdown(f"## {current_project_file_name}")

progress = st.progress(0, "Parsing...")
error_log = st.expander("Error log")

with error_log:
    st.text("Parsing started")
df = _build_basic_stat_df(soup)
with error_log:
    st.text("Parsing finished")

st.dataframe(df)
