from tinydb import TinyDB, where


class TinyWrapper(TinyDB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = args[0]

    def insert_key(self, key, value, table=None):
        if table is None:
            table = self.DEFAULT_TABLE

        self.table(table).upsert(dict(key=key, value=value), where('key') == key)

    def get_key(self, key, table=None, single=False):
        if table is None:
            table = self.DEFAULT_TABLE

        docs = self.table(table).search(where('key') == key)
        if single:
            if len(docs) > 0:
                return docs[0]['value']
        else:
            return [i['value'] for i in docs]
