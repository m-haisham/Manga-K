from tinydb import Query

from modules.database import meta
from modules.database.models import Settings


def get():
    settings = Settings(
        meta.get_key('pdf', table=meta.settings.name, single=True),
        meta.get_key('jpg', table=meta.settings.name, single=True),
    )

    if settings is None:
        s = Settings()
        update(s.to_dict())
        return s
    else:
        return settings


def upsert(key, value):
    meta.insert_key(key, value, table=meta.settings.name)


def update(settings: Settings):
    if type(settings) == dict:
        settings = Settings.from_dict(settings)

    meta.insert_key('pdf', settings.pdf, table=meta.settings.name)
    meta.insert_key('jpg', settings.jpg, table=meta.settings.name)


def check():
    """
    Get keys from settings object
    use keys to create Queries for any match
    apply the queries to settings table
    check if the resulting list is all true
    """
    return all([meta.settings.search(i) for i in [Query().key.any(key) for key in Settings().to_dict().keys()]])
