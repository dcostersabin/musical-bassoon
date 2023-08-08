from db import conn
from typing import Union
from colorama import Fore, Style
from db.models import Model
from db.models import DTYPE
from psycopg2 import OperationalError, DatabaseError


class CRUDBase:
    def __init__(self, model: Model):
        self.model = model
        self.conn = conn

    @property
    def fields(self) -> set:
        return set([i.name for i in self.model().fields])

    def _get_valid_fields(self, fields: set) -> set:
        return set([i for i in fields if i in self.fields])

    def _format_values(self, valid_fields: set) -> str:
        dtype_map = self.model().dtype_map

        formatted_values = []
        for field in valid_fields:
            if (
                dtype_map.get(field) is DTYPE.VARCHAR
                or dtype_map.get(field) is DTYPE.FOREIGN
                or dtype_map.get(field) is DTYPE.DATETIME
            ):
                formatted_values.append("%s")
            else:
                formatted_values.append("%d")
        return ",".join(formatted_values)

    def _execute_query(self, query: str, values: tuple) -> Union[list, None]:
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, values)
                self.conn.commit()

                print(f"{Fore.GREEN} Query Executed {query}{Style.RESET_ALL}")
                try:
                    rowdicts = []
                    cols = list(map(lambda x: x[0], cursor.description))
                    for row in cursor.fetchall():
                        newdict = {}
                        for name, val in zip(cols, row):
                            newdict[name] = val
                        rowdicts.append(newdict)
                    return rowdicts
                except TypeError:
                    return None

            except (OperationalError, DatabaseError, Exception) as e:
                print(e)
                print(f"{Fore.RED} Could Not Execute Query {query}{Style.RESET_ALL}")

    def insert(self, data: dict):
        model = self.model()

        valid_fields = self._get_valid_fields(fields=set(data.keys()))
        formatted_valid_fields = ", ".join(valid_fields)
        formatted_valid_values = self._format_values(valid_fields=valid_fields)
        values = tuple([data.get(i) for i in valid_fields])

        query = f"INSERT INTO app_{model.tname}({formatted_valid_fields}) VALUES ({formatted_valid_values});"
        self._execute_query(query=query, values=values)

    def delete(self, id: str):
        query = f"DELETE FROM app_{self.model().tname} WHERE id = %s;"
        values = (id,)
        self._execute_query(query=query, values=values)

    def get_one(self, id: str):
        query = f"SELECT * FROM app_{self.model().tname} WHERE id = %s;"
        values = (id,)
        data = self._execute_query(query=query, values=values)
        return data[0] if len(data) > 0 else None

    def all(self, page_number=1, page_size=10, order_by="id", dec=True):
        offset = (page_number - 1) * page_size

        order_by = order_by if order_by in self.fields else "id"

        sort_type = "DESC" if dec else "AES"
        order_by_query = f"ORDER BY {order_by} {sort_type}"

        query = f"SELECT * FROM app_{self.model().tname} {order_by_query} OFFSET {int(offset)} LIMIT {int(page_size)} ;"
        values = (offset, page_size)
        return self._execute_query(query=query, values=values)
