import os
import pandas as pd
import sys
print('Creating database tables for Family Recipes app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    print('os.curdir', os.path.abspath(os.curdir))
    sys.path.append(os.path.abspath(os.curdir))

from docmanage import db, bcrypt, create_app
from docmanage.models import User, Role

app = create_app()
ctx = app.app_context()
ctx.push()

file = os.path.abspath("instance/users.xlsx")
users = pd.read_excel(file)

for index, data in users.iterrows():
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    testUser = User(
        firstname=data["firstname"],
        lastname=data["lastname"],
        company=data["company"],
        jobtitle=data["jobtitle"],
        username=data["username"],
        email=data["email"],
        password=hashed_password,
        country_id=data["country_id"]
    )
    role = Role.query.filter_by(rolename="user").first()
    if not role:
        role = Role(rolename="user")
    testUser.roles.append(role)
    role.users.append(testUser)
    db.session.add(testUser)
    db.session.add(role)
db.session.commit()
