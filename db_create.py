from views import db
from models import Task
from datetime import date

# create the database and the db table
db.create_all()

# insert data
# db.session.add(Task("Finish the tutorial", date(2015, 3, 13), 10, 1))
# db.session.add(Task("Finish Real Python", date(2015, 3, 13), 10, 1))

# commit changes
db.session.commit()
