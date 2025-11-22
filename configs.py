import os
import uuid
import logging

import streamlit as st

PROJECT_DIR = "./.local"

SESSION_UUID_ENUM = "uuid"
SESSION_RELATED_PROJECTS_ENUM = "related_projects"
SESSION_CURRENT_PROJECT_ENUM = "current_project"

# -----
# Prepare environment for launch
# -----
if SESSION_RELATED_PROJECTS_ENUM not in st.session_state:
    # file name -> path
    st.session_state[SESSION_RELATED_PROJECTS_ENUM] = {}

if SESSION_UUID_ENUM not in st.session_state:
    st.session_state[SESSION_UUID_ENUM] = uuid.uuid4().hex
SESSION_UUID = st.session_state[SESSION_UUID_ENUM]

if SESSION_CURRENT_PROJECT_ENUM not in st.session_state:
    st.session_state[SESSION_CURRENT_PROJECT_ENUM] = None


SESSION_PROJECT_DIR = os.path.join(PROJECT_DIR, SESSION_UUID)
if not os.path.exists(PROJECT_DIR):
    os.mkdir(PROJECT_DIR)
    logging.info(f"Projects dir created, {PROJECT_DIR}")

if not os.path.exists(SESSION_PROJECT_DIR):
    os.mkdir(SESSION_PROJECT_DIR)
    logging.info(f"Session projects dir created, {SESSION_PROJECT_DIR}")
