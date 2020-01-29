from rest import Rest, api
from flask import Flask

from database.access import DownloadAccess

app = Flask(__name__)
Rest.set(app)
api.setup()


if __name__ == '__main__':
    DownloadAccess.load_from_database()

    app.run(debug=True, use_reloader=False)
