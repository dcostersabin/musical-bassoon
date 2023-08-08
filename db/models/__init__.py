from enum import Enum


class DTYPE(Enum):
    INT = "INT"
    VARCHAR = "VARCHAR"
    DATETIME = "TIMESTAMP"
    FOREIGN = "REFERENCES"


class Field:
    def __init__(self, name, dtype: str, primary=False):
        self.name = name
        self.dtype = dtype


class CharField(Field):
    def __init__(self, name, length=256):
        super(CharField, self).__init__(
            name=name,
            dtype=DTYPE.VARCHAR,
        )
        self.length = length


class IntField(Field):
    def __init__(self, name):
        super(IntField, self).__init__(name=name, dtype=DTYPE.INT)


class DateTimeField(Field):
    def __init__(self, name):
        super(DateTimeField, self).__init__(name=name, dtype=DTYPE.DATETIME)


class Model:
    def __init__(self, tname: str):
        self.fields = set()
        self.tname = tname.lower()

    @property
    def dtype_map(self):
        return {i.name: i.dtype for i in self.fields}


class ForeignKeyField(Field):
    def __init__(self, name, references: Model):
        super(ForeignKeyField, self).__init__(
            name=name,
            dtype=DTYPE.FOREIGN,
        )
        self.references = references
