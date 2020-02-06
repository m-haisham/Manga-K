from tinydb import TinyDB, where
from tinyrecord import transaction


class KeyDB(TinyDB):
    """
    Add key-value feature to database
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = args[0]

    def insert_key(self, key, value, table=TinyDB.DEFAULT_TABLE):
        """
        :param key: position
        :param value: data
        :param table: data table to insert
        :return: None
        """
        table = self.table(table)
        with transaction(table):
            table.upsert(dict(key=key, value=value), where('key') == key)

    def get_key(self, key, table=TinyDB.DEFAULT_TABLE):
        """
        :param key: key to match
        :param table: table to search in

        :returns: array of values if single is false else returns first value
        """
        table = self.table(table)
        with transaction(table):
            item = table.get(where('key') == key)
            if item is None:
                raise KeyError

            return item['value']

    def remove_key(self, key, table=TinyDB.DEFAULT_TABLE):
        """
        Removes all the docs with value key

        :param key: key to match
        :param table: table to remove in
        :return: None
        """
        table = self.table(table)
        with transaction(table):
            table.remove(where('key') == key)
