import os
import logging
from functools import partial

import streamlit as st

import configs

logging.basicConfig(level=logging.INFO)
logging.info("App loading")


def _upload_file_widget():
    # Load project and save for analysis
    uploaded_file = st.file_uploader(
        "Choose a file", type=["l5x"], help="Do not upload harmful content pls."
    )
    if uploaded_file is not None:
        logging.info("File upload started")

        file_name = uploaded_file.name
        file_path = os.path.join(configs.SESSION_PROJECT_DIR, file_name).replace(
            "\\", "/"
        )
        logging.info(f"{file_name}, {file_path}")

        bytes_data = uploaded_file.getvalue()
        with open(file_path, "wb") as f:
            f.write(bytes_data)

        st.session_state[configs.SESSION_RELATED_PROJECTS_ENUM][file_name] = file_path
        logging.info("File upload finished")


def _list_available_projects():
    def load_project_by_file_name(name: str):
        logging.info(f"Request to load project {name}")
        st.session_state[configs.SESSION_CURRENT_PROJECT_ENUM] = name

    def delete_project_by_file_name(name: str):
        logging.info(f"Request to delete project {name}")
        try:
            os.remove(st.session_state[configs.SESSION_RELATED_PROJECTS_ENUM][name])
        except KeyError:
            logging.info("Project does not exist in session")
            return
        except OSError:
            logging.info("Project files do not exist")
            pass
        del st.session_state[configs.SESSION_RELATED_PROJECTS_ENUM][name]

    if len(st.session_state[configs.SESSION_RELATED_PROJECTS_ENUM]):
        st.markdown("### List of your projects")
        for file_name in st.session_state[configs.SESSION_RELATED_PROJECTS_ENUM].keys():
            c1, c2, c3 = st.columns([9, 2, 1])
            with c1:
                st.markdown(f"`{file_name}`")
            with c2:
                st.button(
                    "Load",
                    on_click=partial(load_project_by_file_name, file_name),
                    use_container_width=True,
                )
            with c3:
                st.button(
                    "**X**",
                    on_click=partial(delete_project_by_file_name, file_name),
                    use_container_width=True,
                )
    else:
        st.info("No projects")
    st.markdown(
        f"**Current project**: `{st.session_state[configs.SESSION_CURRENT_PROJECT_ENUM] or 'not loaded'}`"
    )


st.markdown("## LOGIC BLENDER")
st.markdown("*A place where broken things are analyzed*")

_upload_file_widget()
_list_available_projects()
