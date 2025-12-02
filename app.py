import argparse
import logging

import configs
from sources.utils import load_project_as_xml
from sources.project_overview import explore_basic_statistics

parser = argparse.ArgumentParser(
    prog=configs.PROGRAM_TITLE.capitalize(),
    description="PLC code structural analysis",
    epilog="Think twice, force once",
)

parser.add_argument("project_file")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()
project_file: str = args.project_file

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
logging.info(f"---| {configs.PROGRAM_TITLE.upper()} |---()---(\\)---(L)\n")


logging.info(f"Openning: {project_file}")
project_xml = load_project_as_xml(path=project_file)

explore_basic_statistics(project_xml=project_xml)
