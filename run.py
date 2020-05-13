"""
This module is to run application for doc_management
"""

from docmanage import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

"""
from docmanage import db, create_app
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
exit()
"""