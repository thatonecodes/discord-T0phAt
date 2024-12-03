import dotenv 
import os
dotenv.load_dotenv(dotenv.find_dotenv())

def getenv(var: str):
    name = os.getenv(var)
    if not name:
        return None
    return name

