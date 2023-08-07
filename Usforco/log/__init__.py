from datetime import datetime
import os

def log(i, cmd):
    date = datetime.now()
    day = f"{date.day}-{date.month}-{date.year}"
    log_time = f'{date.hour}:{date.minute}:{date.second}'
    with open(f"{os.getcwd()}\\log\\log\\{day}.txt", "a+", encoding="utf8") as file:
        file.write(f"{log_time}   :  {i.user.id} - {i.user} EXECUTED CMD : {cmd}\n")