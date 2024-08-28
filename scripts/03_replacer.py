import os
import pytz
from pathlib import Path
from loguru import logger
from datetime import datetime

# Path Configs
CONFIG_PATH = Path(os.environ.get("MAP_CONFIG_PATH"))

# HTML Web
HTML_WEB_SITENAME = os.environ.get("HTML_WEB_SITENAME")
HTML_WEB_CONTENT = os.environ.get("HTML_WEB_CONTENT")
HTML_TITLE = os.environ.get("HTML_TITLE")

# Web data path
WEB_PATH = CONFIG_PATH.joinpath("web")
WEB_INDEX_PATH = WEB_PATH.joinpath("index.html")
LANG_EN_PATH = WEB_PATH.joinpath("lang/en.conf")
LANG_ZH_TW_PATH = WEB_PATH.joinpath("lang/zh_TW.conf")

# Misc
MC_VERSION = os.environ.get("MC_VERSION")
EXTRA_INFO_OPEN_TIME = os.environ.get("EXTRA_INFO_OPEN_TIME")
EXTRA_INFO_FLAG = os.environ.get("EXTRA_INFO_FLAG")

def replacer(old_string: str, new_string: str, path: Path):
    data = path.read_text()
    new_data = data.replace(old_string, new_string)
    path.write_text(new_data)
    logger.success(f"FileName: {path.name}.")
    logger.success(f"- Replace '{old_string}' to '{new_string}'")

def run_html_replace():
    HTML_REPLACE_LIST = [
        ('content="BlueMap is a tool that generates 3D maps of your Minecraft worlds and displays them in your browser"', 
        f'content="{HTML_WEB_CONTENT}"'
        ),
        ('name="og:site_name" content="BlueMap"',
        f'name="og:site_name" content="{HTML_WEB_SITENAME}"'
        ),
        ('name="og:title" content="BlueMap"',
        f'name="og:title" content="{HTML_TITLE}"'
        ),
        ('<title>BlueMap</title>',
        f'<title>{HTML_TITLE}</title>'
        )
    ]
    for old, new in HTML_REPLACE_LIST:
      replacer(old, new, WEB_INDEX_PATH)

def run_info_replace():
    def current_date() -> str:
        tz = pytz.timezone("Asia/Taipei")
        current_time = datetime.now(tz)
        logger.debug(current_time)
        formatted_time = current_time.strftime("%Y/%m/%d %H:%M")
        logger.debug(formatted_time)
        return formatted_time

    info_format_zh_tw = f"""
  這張地圖用 &#9829; 產生，使用 <a href="https://bluecolo.red/bluemap">BlueMap</a> {{version}}<br/>
  建構於 {current_date()}<br/>
  繪製版本 {MC_VERSION}<br/>
  開服時間 {EXTRA_INFO_OPEN_TIME}<br/>
  <img src="https://img.shields.io/badge/netlify-%23000000.svg?style=for-the-badge&logo=netlify&logoColor=#00C7B7" alt"Powered by Netlify"/><br/>
  {EXTRA_INFO_FLAG}
"""
    info_format_en = f"""
  This map has been generated with &#9829; using <a href="https://bluecolo.red/bluemap">BlueMap</a> {{version}}<br/>
  Build at {current_date()}<br/>
  Render Version {MC_VERSION}<br/>
  Open Time {EXTRA_INFO_OPEN_TIME}<br/>
  <img src="https://img.shields.io/badge/netlify-%23000000.svg?style=for-the-badge&logo=netlify&logoColor=#00C7B7" alt"Powered by Netlify"/><br/>
  {EXTRA_INFO_FLAG}
"""
    replacer("{placeholder_zh_tw}", f"{info_format_zh_tw}", LANG_ZH_TW_PATH)
    replacer("{placeholder_en}", f"{info_format_en}", LANG_EN_PATH)

def main():
   run_html_replace()
   run_info_replace()

main()