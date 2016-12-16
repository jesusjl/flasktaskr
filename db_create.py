# db_create.py
from datetime import date

from project import db, bcrypt
from project.models import User, Task

# create the database and the db table
db.create_all()

# insert data
db.session.add(
    User("admin", "admin@admin.com",
         bcrypt.generate_password_hash("admin"), "admin")
)

db.session.add(
    Task("Finish the tutorial", date(2015, 3, 13), 10, date(2015, 2, 13), 1, 1)
)

db.session.add(
    Task("Finish Real Python", date(2015, 3, 13), 10, date(2015, 2, 13), 1, 1)
)

# commit changes
db.session.commit()
