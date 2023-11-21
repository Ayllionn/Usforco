import json
import traceback

import conf


def list_all_db_name() -> list:
    with open(conf.DB) as file:
        names = []
        for name in json.load(fp=file):
            names.append(name)
    return names


class DB:
    def __init__(self, db_name: str):
        self._name = db_name
        self.content = None
        self._refresh()

    def end(self):
        self.content = None

    def _refresh(self):
        try:
            with open(conf.DB) as file:
                self.content = json.load(fp=file)
                self.content = self.content[self._name]
            if len(self.content) <= 0:
                self.content = None
        except:
            self.content = None

    def write(self):
        with open(conf.DB, "r+", encoding="utf8") as file:
            try:
                db = json.load(fp=file)
            except:
                traceback.print_exc()
                db = {}

        if self.content is not None:
            db.update({self._name: self.content})
        else:
            db.pop(self._name)

        with open(conf.DB, "w+", encoding="utf8") as file:
            json.dump(obj=db, fp=file)

        self._refresh()

    def sup(self):
        self.content = None
        self.write()
        self._refresh()

    def if_not_exist(self):
        if self.content is None:
            return True
        else:
            return False

    def get(self, *args: str, error=False):
        self._refresh()
        if self.if_not_exist():
            return None, 1
        else:
            db = self.content
            for i in args:
                if type(i) is str:
                    db = db.get(i)
                else:
                    try:
                        db = db.get(str(i))
                    except:
                        if error:
                            return db, 1
                        return db
                if db is None:
                    if error:
                        return db, 1
                    raise db

            if error:
                return db, 0
            return db

    def update(self, data: dict = {}, **kwargs):
        self._refresh()
        if self.if_not_exist():
            return self.set(**data, **kwargs)
        else:
            try:
                self.content.update(data)
            except Exception as e:
                return str(e)

            self.content.update({**data, **kwargs})
            self.write()

            return 0

    def clear_all(self):
        self._refresh()
        self.content = None
        self.write()

        return 0

    def remove(self, *args:str):
        for k in args:
            self._refresh()
            self.content.pop(k)
            self.write()

        return 0

    def set(self, db: dict = {}, **kwargs):
        if type(db) is not dict:
            raise ValueError("Ce doit être un dictionnaire")

        self.content = {**db, **kwargs}
        self.write()

        return 0