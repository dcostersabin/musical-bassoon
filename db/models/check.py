from db import conn
from ordered_set import OrderedSet
from db.models import Model
from db.models.generate_table import TableGenerator


class CheckTables:
    def __init__(self, models: OrderedSet[Model]):
        self.conn = conn
        self.models = models

    def start(self):
        self._run()

    def _run(self):
        self._check_tables()

    @property
    def tables(self) -> list:
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT tablename FROM pg_catalog.pg_tables "
                + "WHERE tablename LIKE 'app_%';"
            )
            total_tables = [i[0] for i in cursor.fetchall()]
        return OrderedSet(total_tables)

    def _check_tables(self):
        table_dict = {f"app_{i().tname}": i for i in self.models}
        tables_in_config = OrderedSet([i for i in table_dict.keys()])
        tables_in_db = self.tables
        difference = tables_in_config - tables_in_db
        tables_to_create = [table_dict.get(i) for i in difference]
        TableGenerator(models=tables_to_create).start()
