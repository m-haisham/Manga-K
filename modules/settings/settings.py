from tinydb import Query

from modules.database import meta
from modules.database.models import Settings


def get():
        params = list(Settings().todict().keys())

        sdict = {
            param: meta.get_key(param, table=meta.settings.name, single=True) for param in params
        }

        if any(list(map(lambda val: sdict[val] is None, sdict.keys()))):
            s = Settings()
            update(s.todict())
            return s

        return Settings.fromdict(sdict)

def upsert(key, value):
    """
    Insert (Update if exists) the key-value pair
    :param key: identifier
    :param value: data
    :return: None
    """
    meta.insert_key(key, value, table=meta.settings.name)


def update(settings: dict or Settings):
    """
    Update the datastore for settings
    :param settings: data
    :return: None
    """
    # to dict format
    if type(settings) == Settings:
        settings = settings.todict()

    # loop all keys
    for key in settings.keys():
        upsert(key, settings[key])


def check():
    """
    Get keys from settings object
    use keys to create Queries for any match
    apply the queries to settings table
    check if the resulting list is all true
    """
    return all([meta.settings.search(i) for i in [Query().key.any(key) for key in Settings().todict().keys()]])
