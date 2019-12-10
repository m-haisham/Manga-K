import shutil
import sys

from modules.console import confirm
from modules.ui import Loader
from ..database import meta
from ..mangas import manga
from modules.database.mangas import base
from ..paths import base_directory


def reset():
    cont = confirm('This will REMOVE all your data and close app, would you still like to continue?', default=False)

    if cont:
        with Loader("Erase data"):

            # unlink all databases so they are not being used anymore
            base.close()
            meta.close()

            for key, database in manga.databases.items():
                database.close()

            # unlink the files and exit
            shutil.rmtree(base_directory)
            sys.exit(1)
