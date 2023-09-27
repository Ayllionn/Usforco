import os
from json import dump, load

BAS_DIR = os.getcwd()


def get(db_name, *args:list):
    try:
        with open(f"{BAS_DIR}/files_json/{db_name}.json", "r+") as f:
            data = load(f)

            for dt in args:
                data = data[dt]
        keys = args
        return data, keys
    except:
        return None, None


def modify(db_name, data:dict):
    with open(f"{BAS_DIR}/files_json/{db_name}.json", "w") as f:
        dump(data, f)


def update(db_name, news:dict):
    f = open(f'{BAS_DIR}/files_json/{db_name}.json', "r+")
    data : dict = load(f)
    f.close()

    data.update(news)
    if len(data) > 0:
        dump(data, open(f'{BAS_DIR}/files_json/{db_name}.json', "w"))
    else:
        os.system(f"rm {BAS_DIR}/files_json/{db_name}.json")