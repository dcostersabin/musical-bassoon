from db.models import Model
from abc import ABC, abstractmethod
from db.models import CharField, DateTimeField, IntField, ForeignKeyField


class QueryGenerator(ABC):
    def __init__(self, model: Model):
        self.model = model

    @property
    def get_char_fields(self):
        char_fields = [
            i
            for i in self.model.fields
            if isinstance(
                i,
                CharField,
            )
        ]
        query = [f"{i.name} {i.dtype.value}({i.length})" for i in char_fields]
        return ",".join(query)

    @property
    def get_timestamp_fields(self):
        timestamp_fields = [
            i
            for i in self.model.fields
            if isinstance(
                i,
                DateTimeField,
            )
        ]
        query = [f"{i.name} {i.dtype.value}" for i in timestamp_fields]
        return ",".join(query) if len(query) > 1 else ""

    @property
    def get_primary_key(self):
        return "id serial NOT NULL PRIMARY KEY"

    @property
    def get_int_fields(self):
        int_fields = [
            i
            for i in self.model.fields
            if isinstance(
                i,
                IntField,
            )
        ]
        query = [f"{i.name} {i.dtype.value}" for i in int_fields]
        return ",".join(query) if len(query) > 1 else ""

    @property
    def get_foreign_keys(self):
        foreign_keys = [
            i
            for i in self.model.fields
            if isinstance(
                i,
                ForeignKeyField,
            )
        ]
        query = [
            f"{i.name} int {i.dtype.value} {i.references.tname}(id)"
            for i in foreign_keys
        ]
        return ",".join(query) if len(query) > 1 else ""

    @abstractmethod
    def generate_query(self) -> str:
        return ""


class CreateQueryGenerator(QueryGenerator):
    def __init__(self, model: Model):
        super(CreateQueryGenerator, self).__init__(model=model)

    def generate_query(self) -> str:
        queries = [
            self.get_foreign_keys,
            self.get_char_fields,
            self.get_timestamp_fields,
            self.get_int_fields,
        ]
        str_queries = ",".join([i for i in queries if len(i) > 1])
        return (
            f"CREATE TABLE app_{self.model.tname}({self.get_primary_key},"
            f"{str_queries}"
            f");"
        )
