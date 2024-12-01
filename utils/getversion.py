from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
version = os.getenv("VERSION")
def getVersion() -> str:
    if not version:
        return "Not Found"
    return version
