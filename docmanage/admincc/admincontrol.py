"""
this module to ccontrol the access for flaskadmin
"""

from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('users.login', next=request.url))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.is_admin()
    # https://www.youtube.com/watch?v=NYWEf9bZhHQ
