from flask_restful import reqparse


offline_parser = reqparse.RequestParser()
offline_parser.add_argument('offline', type=bool, default=False)

limit_parser = reqparse.RequestParser()
limit_parser.add_argument('limit', type=int)