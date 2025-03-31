from typing import Optional
from discord import File
from pathlib import Path
from datetime import datetime

def getFile(filename: str, defaultFilename="default.jpg"):
    """
    Retrieves a file for Discord's File object.
    ---
    Attributes:
        filename `str`: The path to the file to be opened.
        defaultFilename `str, optional`: The filename to be used when sending the file. Defaults to "default.jpg".

    Returns:
        `File | None`: A `discord.File` object if the file exists, otherwise `None`.

    Raises:
        `FileNotFoundError`: If the specified file does not exist.
    """
    try:
        with open(filename, "rb") as img:
            return File(img, filename=defaultFilename)
    except FileNotFoundError:
        print(f"ERR: File not found! Check if the file '{filename}' exists.")
        return None

def create_debug_file(path: Path = Path.cwd(), filename: str = "debug.log"):
    """
    Creates a debug log file at the specified path.
    ---
    Attributes: 
        path `Path`: The path specified using pathlib, defaults to `Path.cwd()`
        filename `str`: The filename you would like to call the debug file, default is "debug.log"

    Returns:
        `Path`: The path of the created log file.

    Raises:
        `FileExistsError`: If the file already exists
    """
    
    target_path = path if path else Path.cwd()
    target_path = Path(target_path)

    log_file = target_path / filename #combine the two
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

    if not log_file.exists():
        with open(log_file, "w") as file:
            file.write(f"{log_file} successfully created at: {current_time}\n")

    return log_file

def remove_debug_file(path: Path = Path.cwd(), filename: str = "debug.log"):
    """
    Removes a debug log file at the specified path.
    ---
    Attributes: 
        path `Path`: The path specified using pathlib, defaults to `Path.cwd()`
        filename `str`: The filename you would like to call the debug file, default is "debug.log"

    Raises:
        `FileNotFoundError`: If the file to delete was not found
    """

    target_path = path if path else Path.cwd()
    target_path = Path(target_path)

    log_file = target_path / filename

    if log_file.exists():
        log_file.unlink()  # Deletes the file
    else:
        raise FileNotFoundError(f"File not found: {log_file}")
