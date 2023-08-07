from db import conn
from colorama import Style, Fore
from db.models import Model
from ordered_set import OrderedSet
from psycopg2 import OperationalError, DatabaseError
from db.models.query_generator import CreateQueryGenerator


class TableGenerator:
    def __init__(self, models: OrderedSet[Model]):
        self.conn = conn
        self.models = models

    def start(self):
        self._run()

    def _run(self):
        self._create_tables()

    def _create_tables(self):
        for model in self.models:
            model = model()
            query = CreateQueryGenerator(model=model).generate_query()
            with self.conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    self.conn.commit()
                    print(
                        f"Table {model.tname} {Fore.GREEN} Generated Successfully {Style.RESET_ALL}"
                    )
                except (OperationalError, DatabaseError, Exception) as e:
                    print(
                        f"{Fore.RED} Could Not Create Table{Style.RESET_ALL} {model.tname}"
                    )
