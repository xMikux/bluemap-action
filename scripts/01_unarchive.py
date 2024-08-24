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

def unarchive_folders(folder_list):
    logger.info("Extract folders...")
    with tarfile.open(CONFIG_PATH_ARCHIVE, "r:gz") as tar:
        for member in tar.getmembers():
            if any(member.name.startswith(folder) for folder in folder_list):
                # logger.success(f"Success unarchive {member.name}")
                tar.extract(member, path=MAPS_WORKDIR, filter=None)

def get_directory_size(directory: Path):
    total_size = 0
    for file in directory.rglob('*'):
        if file.is_file():
            total_size += file.stat().st_size
    return total_size

def convert_size(size_in_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = size_in_bytes
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"

def log_dirs_size(folder_list):
    for i in folder_list:
        dir_path = MAPS_WORKDIR.joinpath(i)
        dir_size = convert_size(get_directory_size(dir_path))
        logger.info(f"{i} directory size is {dir_size}")

def main():
    maps_list = MAPS_LIST_STR.split()
    logger.debug(maps_list)
    MAPS_WORKDIR.mkdir()
    unarchive_folders(maps_list)
    log_dirs_size(maps_list)
    logger.info("Remove backup file.")
    CONFIG_PATH_ARCHIVE.unlink()

main()