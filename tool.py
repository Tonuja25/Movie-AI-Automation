import requests
from datetime import datetime
def addNumbers(a:int, b:int) -> int:
    """
    addition of two numbers
    """
    return a + b
def MultiplyNumbers(a:int, b:int) -> int:
    """
    Multiply of two numbers
    """
    return a * b

def subtractNumbers(a:int, b: int) -> int:
    """
    subtract of two numbers
    
    """
    return a - b

def saveFile(content:str) -> str:
    """
    save file to local system i.e hello.text
    """
    with open("./hello.txt","w+") as file:
        file.write(content)
        file.close()
        return "file  created and saved successfully"

def readFile() -> str:
    """
    reading file created file i.e hello.text
    """
    with open('./hello.txt',"r+") as file:
        data = file.read()
        file.close()
        return "File content:"+ data
def clientIP() -> str:
    """
    show client public IP Address
    """
    response = requests.get("https://api.ipify.org")
    return "Client IP Address:" + response.text

def getCurrentTime () -> str:
    """
    show current Time HH::MMM:SS AM/PM Format
    """
    current_time = datetime.now().strftime("%I:%M:%S:%p") 
    return "Current Time:" + current_time