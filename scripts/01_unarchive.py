import os
import tarfile
from pathlib import Path
from loguru import logger

# Path Configs
CONFIG_PATH = Path(os.environ.get("MAP_CONFIG_PATH"))
CONFIG_PATH_ARCHIVE = CONFIG_PATH.joinpath("server-backup.tar.gz")

# Maps Configs
MAPS_WORKDIR = CONFIG_PATH.joinpath("Maps")
MAPS_LIST_STR = os.environ.get("MAPS_LIST")

test_extract = ["world_nether", "world_the_end"]

def unarchive_folders(folder_list):
    with tarfile.open(CONFIG_PATH_ARCHIVE, "r:gz") as tar:
        for member in tar.getmembers():
            if any(member.name.startswith(folder) for folder in folder_list):
                logger.success(f"Success unarchive {member.name}")
                tar.extract(member, path=MAPS_WORKDIR, filter=None)

def main():
    maps_list = MAPS_LIST_STR.split()
    logger.debug(maps_list)
    MAPS_WORKDIR.mkdir(exist_ok=True)
    unarchive_folders(maps_list)

main()