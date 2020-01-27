from rest import Rest, api
from flask import Flask

app = Flask(__name__)
Rest.set(app)
api.setup()

if __name__ == '__main__':
    app.run(debug=True)
