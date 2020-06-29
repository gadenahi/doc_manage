import os
import sys


print('Creating database tables for Family Recipes app...')

if os.path.abspath(os.curdir) not in sys.path:
    print('...missing directory in PYTHONPATH... added!')
    print('os.curdir', os.path.abspath(os.curdir))
    sys.path.append(os.path.abspath(os.curdir))


from docmanage import db, create_app
from docmanage.models import Order
import pandas as pd


app = create_app()
ctx = app.app_context()
ctx.push()

orders = pd.read_excel('instance/orders.xlsx')

for index, order in orders.iterrows():
    test_order = Order(
        user_id=order['user_id'],
        report_id=order['report_id'],
        order_price=order['order_price'],
        date_order=order['date_order'] # also need to change the models
    )
    db.session.add(test_order)
db.session.commit()
