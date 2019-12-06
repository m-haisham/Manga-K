from tinydb import TinyDB, where, Query


class TinyWrapper(TinyDB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = args[0]

    def insert_key(self, key, value, table=TinyDB.DEFAULT_TABLE):
        self.table(table).upsert(dict(key=key, value=value), where('key') == key)

    def get_key(self, key, table=TinyDB.DEFAULT_TABLE, single=False):
        docs = self.table(table).search(where('key') == key)
        if single:
            if len(docs) > 0:
                return docs[0]['value']
        else:
            return [i['value'] for i in docs]

    def remove_key(self, key, table=TinyDB.DEFAULT_TABLE):
        self.table(table).remove(where('key') == key)