import dotenv 
import os
dotenv.load_dotenv(dotenv.find_dotenv())
name = os.getenv("BOTNAME")

def getName() -> str:
    if not name:
        return ""
    return name

