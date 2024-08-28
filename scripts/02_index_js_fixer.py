import os
from pathlib import Path
from loguru import logger

# Path Configs
CONFIG_PATH = Path(os.environ.get("MAP_CONFIG_PATH"))

# Web data path
WEB_PATH = CONFIG_PATH.joinpath("web")
WEB_INDEX_PATH = next((i for i in WEB_PATH.rglob("index-*.js")), None)
logger.info(f"Index path is {WEB_INDEX_PATH}")

# Replace List
REPLACE_LIST = [
    ("\".prbm\"", "\".prbm.gz\""),
    ("\"textures.json\"", "\"textures.json.gz\"")
]

def run_replace(old_string: str, new_string: str):
    js_data = WEB_INDEX_PATH.read_text()
    new_js_data = js_data.replace(old_string, new_string)
    WEB_INDEX_PATH.write_text(new_js_data)
    logger.success(f"Replace {old_string} to {new_string}!")

for old, new in REPLACE_LIST:
    run_replace(old, new)
