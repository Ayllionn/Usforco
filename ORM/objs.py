import datetime


class DateTimeNow:
    def __init__(self, value=None):
        self.value = value

    def set(self):
        return datetime.datetime.now()

    def get(*args):
        return f"{datetime.datetime.now().day}-{datetime.datetime.now().month}-{datetime.datetime.now().year} " \
              f"{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}"

class ID:
    def __init__(self, value=None):
        self.value = value