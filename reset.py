from database import Database
db = Database.get()

db.drop_all()
db.create_all()