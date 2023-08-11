from db import conn
from typing import Union
from colorama import Fore, Style
from db.models import Model
from db.models import DTYPE
from psycopg2 import OperationalError, DatabaseError, IntegrityError


class CRUDBase:
    def __init__(self, model: Model):
        self.model = model
        self.conn = conn
        self.errors = set()

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
                or field == "id"
            ):
                formatted_values.append("%s")
            else:
                formatted_values.append("%d")
        return ",".join(formatted_values)

    def _execute_query(self, query: str, values: tuple) -> Union[list, None]:
        with self.conn.cursor() as cursor:
            self.errors.clear()
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
            except IntegrityError as e:
                print(e)
                self.errors.add(IntegrityError)
                self.conn.rollback()
                self.conn.commit()
            except DatabaseError as e:
                print(e)
                self.errors.add(DatabaseError)
            except (OperationalError, Exception) as e:
                print(e)
                self.errors.add(OperationalError)
                print(f"{Fore.RED} Could Not Execute Query {query}{Style.RESET_ALL}")
            finally:
                cursor.close()

    def insert(self, data: dict):
        model = self.model()

        valid_fields = self._get_valid_fields(fields=set(data.keys()))
        formatted_valid_fields = ", ".join(valid_fields)
        formatted_valid_values = self._format_values(valid_fields=valid_fields)
        values = tuple([data.get(i) for i in valid_fields])

        query = f"INSERT INTO app_{model.tname}({formatted_valid_fields}) VALUES ({formatted_valid_values}) RETURNING id as id;"
        insert_id = self._execute_query(query=query, values=values)
        if insert_id is None:
            return None
        return insert_id[0] if len(insert_id) > 0 else {"id": None}

    def delete(self, id: str):
        query = f"DELETE FROM app_{self.model().tname} WHERE id = %s;"
        values = (id,)
        self._execute_query(query=query, values=values)

    def get_one(self, id: str):
        query = f"SELECT * FROM app_{self.model().tname} WHERE id = %s LIMIT 1;"
        values = (id,)
        data = self._execute_query(query=query, values=values)
        return data[0] if len(data) > 0 else None

    def all(self, page_number=1, page_size=10, order_by="id", dec=True):
        offset = (page_number - 1) * page_size

        order_by = order_by if order_by in self.fields else "id"

        sort_type = "DESC" if dec else "ASC"
        order_by_query = f"ORDER BY {order_by} {sort_type}"

        query = f"SELECT * FROM app_{self.model().tname} {order_by_query} OFFSET {int(offset)} LIMIT {int(page_size)} ;"
        return self._execute_query(query=query, values=tuple())

    def update(self, id: str, data: dict):
        valid_fields = self._get_valid_fields(fields=set(data.keys()))
        formatted_values = self._format_values(valid_fields=valid_fields)

        update_query = [
            f"{i}={j}" for i, j in zip(valid_fields, formatted_values.split(","))
        ]

        update_query = ", ".join(update_query)

        query = f"UPDATE app_{self.model().tname} SET {update_query} WHERE id=%s"
        values = [data.get(i) for i in valid_fields]
        values.append(id)
        self._execute_query(query=query, values=values)

    def filter(
        self,
        data: dict,
        condition_and=True,
        page_number=1,
        page_size=10,
        order_by="id",
        dec=True,
    ):
        offset = (page_number - 1) * page_size

        order_by = order_by if order_by in self.fields else "id"

        sort_type = "DESC" if dec else "ASC"
        order_by_query = f"ORDER BY {order_by} {sort_type}"

        valid_fields = self._get_valid_fields(fields=set(data.keys()))

        if "id" in data:
            valid_fields.update({"id"})

        formatted_values = self._format_values(valid_fields=valid_fields)

        where_query = [
            f"{i}={j}" for i, j in zip(valid_fields, formatted_values.split(","))
        ]

        if condition_and:
            where_query = " AND ".join(where_query)
        else:
            where_query = " OR ".join(where_query)

        query = (
            f"SELECT * FROM app_{self.model().tname} WHERE {where_query} {order_by_query} OFFSET "
            f"{int(offset)} LIMIT {int(page_size)};"
        )

        values = tuple([data.get(i) for i in valid_fields])

        return self._execute_query(query=query, values=values)
