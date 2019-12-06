from ..database.models import Settings

from .settings import get, upsert, update, check
from ..console import confirm, format_dict_pair, from_template, title


def change():
    print(title('Current'))
    get().display()

    print(title('New'))
    d = prompt()
    Settings.from_dict(d).display()
    if not confirm('Are you happy with the changes? '):
        print(title("Changes discarded"))
        return

    update(d)


def prompt():
    return from_template(get().to_dict())
