import json
import traceback
from .cmds import create_table, \
    create_table_without_id, get_all_by_a_tables, \
    get_one_by_id, create_donne, delete_donne, update
from .objs import *


class orm:
    def __init__(self):
        self._models = {}
        self.tables = []

    def get_table(self, table_name):
        if table_name in self.tables:
            return self._models[table_name]
        else:
            raise Exception("La table {} n'existe pas".format(table_name))

    def get_all_by_a_table(self, table_name):
        return get_all_by_a_tables(table_name)

    def get_value_by_id(self, table_name, id: int):
        return self._models.get(table_name)(**{k:v for k,v in zip(self._models.get(table_name)()._collums_names,
                                                                  get_one_by_id(table_name, id))})

    def get_obj(self, table_name):
        return self._models[table_name]()

    def Model(self, obj):
        auto_id = False
        master_orm = self
        attributes = vars(obj)
        temp = {}
        collums_names = []
        for attr_name, attr_value in attributes.items():
            try:
                if attr_name.startswith("__"):
                    continue
                if attr_value not in [int, float, str, bool, dict, list, tuple, DateTimeNow, ID]:
                    raise ValueError("Votre modèle en peut comprendre que des valeurs de type : [int, float, str, "
                                     "bool, dict, list, tuple, DateTimeNow, ID]")
                if attr_value == ID:
                    auto_id = True
                temp[attr_name] = attr_value
                collums_names.append(attr_name)
            except:
                traceback.print_exc()
        if auto_id is False:
            create_table(obj.__name__, **temp)
        else:
            create_table_without_id(obj.__name__, **temp)

        class MODEL:
            def __init__(self, *args, **kwargs):
                self._db = master_orm
                self._collums_names = collums_names.copy()
                self._table = obj.__name__
                self._auto_id = auto_id
                self._getted = False
                for attr_name, attr_value in kwargs.items():
                    self._getted = True
                    try:
                        setattr(self, attr_name, json.loads(attr_value))
                    except:
                        setattr(self, attr_name, attr_value)

                try:
                    self._collums_names.remove("id")
                except:
                    pass
                finally:
                    self._collums_names.insert(0, "id")

            def table(self):
                return self._table

            def create(self, **kwargs):
                collums_names = self._collums_names.copy()
                if self._auto_id is False:
                    try:
                        collums_names.remove("id")
                    except:
                        pass
                if len(kwargs.keys()) != len(collums_names):
                    raise ValueError(f"Suffisament de valeur (\n"
                                     f"\t{' / '.join([i for i in kwargs.keys()])},\n"
                                     f"\t{' / '.join(collums_names)}"
                                     f")")
                for k in kwargs.keys():
                    if k not in collums_names:
                        raise ValueError(f"{k} not in {self.collums_names}")
                return MODEL(**{k:v for k, v in zip(self._collums_names, create_donne(table_name=self._table,**kwargs))})

            def get(self, id):
                try:
                    return MODEL(**{k:v for k, v in zip(self._collums_names, get_one_by_id(self._table, id))})
                except:
                    return None

            def delete(self):
                if self._getted:
                    delete_donne(self._table, self.id)
                else:
                    raise ValueError("Object not getted")

            def update(self):
                if self._getted:
                    temp = {}
                    attr = vars(self)
                    for k,v in attr:
                        if k.startswith('_') or k.startswith('__'):
                            continue
                        else:
                            temp.update({k,v})
                    temp.pop("id")
                    update(self._table, self.id, **temp)
                else:
                    raise ValueError("Object not getted")

        self._models.update(
            {obj.__name__: MODEL}
        )
        self.tables.append(obj.__name__)
        return MODEL


ORM = orm()
