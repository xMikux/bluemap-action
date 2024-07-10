import pysftp
import os
from pathlib import Path
from loguru import logger

sftp_host_name = os.getenv("SFTP_HOST_NAME")
sftp_user_name = os.getenv("SFTP_USER_NAME")
sftp_password = os.getenv("SFTP_PASSWORD")
sftp_port = os.getenv("SFTP_PORT", 2022)
maps_list = os.getenv("MAP_LIST").split(" ")

if not Path("Maps").exists():
    Path("Maps").mkdir()

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection(host=sftp_host_name, port=sftp_port, username=sftp_user_name, password=sftp_password, cnopts=cnopts) as sftp:
    for map in maps_list:
        logger.info(f"Downloading Map - {map}...")
        sftp.get_r(map, 'Maps', preserve_mtime=True)
        logger.info(f"Download Done!")
        logger.info("")

logger.info("Finished Download Mpas!")