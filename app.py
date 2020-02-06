from flask import Flask

import database

app = Flask(__name__)
database.set(app)

from rest import Rest, api

Rest.set(app)
api.setup()

if __name__ == '__main__':
    from database.access import DownloadAccess

    DownloadAccess.load_from_database()
    app.run(debug=True, use_reloader=False)
