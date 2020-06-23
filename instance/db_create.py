import sys
import os

print('Creating database tables for Family Recipes app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    print('os.curdir', os.path.abspath(os.curdir))
    sys.path.append(os.path.abspath(os.curdir))

from docmanage import db, create_app, bcrypt
from docmanage.models import User, Role, Country

app = create_app()
ctx = app.app_context()
ctx.push()
db.drop_all()
db.create_all()

countries = ['Japan', 'United States']

for cname in countries:
    country = Country(
        countryname=cname
    )
    db.session.add(country)

db.session.commit()

password = 'admin'
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
user = User(
    firstname="admin",
    lastname="admin",
    company="admin",
    jobtitle="admin",
    username="admin",
    email="admin@test.com",
    password=hashed_password,
    country_id=1
)
role = Role(rolename="admin")
user.roles.append(role)
role.users.append(user)
db.session.add(user)
db.session.add(role)
db.session.commit()


# https://blog.mktia.com/how-to-solve-the-error-that-module-not-found/#toc3
# https://note.nkmk.me/python-relative-import/
# https://gitlab.com/patkennedy79/flask_recipe_app/-/blob/master/web/instance/db_create.py


# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_many_to_many_relationships.htm