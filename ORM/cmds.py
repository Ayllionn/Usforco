import sqlite3
import json
from .objs import *

db = sqlite3.connect("./ORM/db.db")
c = db.cursor()


def converte(typ):
    if typ == int:
        return "INTEGER"
    elif typ == float:
        return "FLOAT"
    elif typ == str:
        return "TEXT"
    elif typ == bool:
        return "INTEGER"
    elif typ == list or typ == dict:
        return "TEXT"
    elif typ == tuple:
        return "TEXT"
    elif typ == ID:
        return "INTEGER PRIMARY KEY"
    else:
        return "TEXT"


def create_table(_name, **kwargs):
    c.execute(
        f"CREATE TABLE IF NOT EXISTS {_name} ("
        f"  id INTEGER PRIMARY KEY AUTOINCREMENT,"
        f"  {','.join([f'{k} {converte(v)}' for k, v in kwargs.items()])}"
        f")"
    )


def create_table_without_id(_name, **kwargs):
    c.execute(
        f"CREATE TABLE IF NOT EXISTS {_name} ("
        f"  {','.join([f'{k} {converte(v)}' for k, v in kwargs.items()])}"
        f")"
    )


def get_all_by_a_tables(table):
    c.execute(f"SELECT * FROM {table}")
    return c.fetchall()


def get_one_by_id(table, value):
    c.execute(f"SELECT * FROM {table} WHERE id = ?", (value,))
    return c.fetchone()


def create_donne(table_name, **kwargs):
    serialized_data = {k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in kwargs.items()}

    columns = ', '.join(serialized_data.keys())
    values = ', '.join(['?' for _ in serialized_data.values()])

    c.execute(
        f"INSERT INTO {table_name} "
        f"({columns}) "
        f"VALUES ({values})",
        tuple(serialized_data.values())
    )
    db.commit()

    last_row_id = c.lastrowid

    return get_one_by_id(table_name, last_row_id)


def delete_donne(table_name, id):
    c.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))
    db.commit()


def update(table_name, id_value, **kwargs):
    serialized_data = {k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in kwargs.items()}
    set_values = ', '.join([f"{key} = ?" for key in serialized_data.keys()])
    values = tuple(serialized_data.values())

    c.execute(f"UPDATE {table_name} SET {set_values} WHERE id = ?", (*values, id_value))
    db.commit()
