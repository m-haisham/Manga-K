from flask import Flask

import database
from rest import Rest, api

# from database.access import DownloadAccess

app = Flask(__name__)
Rest.set(app)
api.setup()

database.set(app)


if __name__ == '__main__':
    # DownloadAccess.load_from_database()

    app.run(debug=True, use_reloader=False)
