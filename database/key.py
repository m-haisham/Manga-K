from tinydb import TinyDB, where


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
        self.table(table).upsert(dict(key=key, value=value), where('key') == key)

    def get_key(self, key, table=TinyDB.DEFAULT_TABLE, single=False):
        """
        :param key: key to match
        :param table: table to search in
        :param single: return first value

        :returns: array of values if single is false else returns first value
        """
        docs = self.table(table).search(where('key') == key)
        if single:
            try:
                return docs[0]['value']
            except IndexError:
                raise KeyError(f'"{key}" not found')
        else:
            return [i['value'] for i in docs]

    def remove_key(self, key, table=TinyDB.DEFAULT_TABLE):
        """
        Removes all the docs with value key

        :param key: key to match
        :param table: table to remove in
        :return: None
        """
        self.table(table).remove(where('key') == key)