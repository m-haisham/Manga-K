from .settings import get, update
from ..console import confirm, from_template, title
from ..database.models import Settings


def change():
    # old
    print(title('Current'))
    old = get()
    old.display()

    # get new
    print()
    print(title('New'))
    d = prompt()

    print()
    Settings.from_dict(d).display()

    if old.to_dict() == d:
        print(title("No changes"))
        return

    # confirm changes
    if not confirm('Are you happy with the changes? '):
        print(title("Changes discarded"))
        return

    update(d)


def prompt():
    return from_template(get().to_dict())
