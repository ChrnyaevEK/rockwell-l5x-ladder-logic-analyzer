import logging
from bs4 import BeautifulSoup


def load_project_as_xml(path: str) -> BeautifulSoup:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return BeautifulSoup(f, features="xml")
    except OSError as e:
        logging.error("Attempt to load project from file failed")
        raise
    except Exception as e:
        logging.error("Attempt to parse project as XML failed")
        raise
