from discord import File
def getFile(filename, defaultFilename="default.jpg"):
    try:
        with open(filename, "rb") as img:
            file = File(img, filename=defaultFilename)

            return file
    except FileNotFoundError:
        print(f"ERR: File not found! Check if file: '{defaultFilename}' exists.")
        return None
