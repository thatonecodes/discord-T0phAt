from dotenv import load_dotenv, find_dotenv
from utils import getFile
import os
from urllib.parse import quote

load_dotenv(find_dotenv())
def getIcon():
    name = "icon.jpg"
    file = getFile(os.getenv("ICON", ""), defaultFilename=name)
    icon_url = f"attachment://{quote(name)}"
    return file, icon_url
