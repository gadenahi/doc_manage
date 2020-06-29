# Report shop site

This is a project for report shopping site using:

- Python3.7.6
- Flask 1.1
- Flask-Admin 1.5.4
- Flask-Mail 0.9.1
- Flask-msearch 0.2.9
- SQLAlchemy 1.3.17
- Numpy 1.18.5
- Pandas 1.0.5
- Matplotlib 3.2.2

This site provides:
- View the report available
- Cart to order multiple reports at the same time
- Proceed the order with the login credential
- Send the email confirmation for the new orders
- Search the report
- Update the account information 
- Management for admin only
    - Upload the list of reports
    - Contacts list
    - Analysis of customer orders by days, months and years
    - Orders summary by report or user
    - Registration for new users as guest
    - Change the status of report either draft or complete
    - Upload report at pdf


## Run
run.py

## To deploy on Heroku
- To install heroku command
    - brew tap heroku/brew && brew install heroku
- To install psycopg2 to use PostgreSQL via SQLAlchemy
    - conda install -c anaconda psycopg2
- To install gunicorn to run on WSGI server for Python
    - conda install -c anaconda gunicorn
- To export requirements (Didn't use pip freeze to avoid including direct references)
    - pip list --format=freeze > requirements.txt
    *Remove some modules if you face some issues during the installation on heroku
- To create Procfile (this command is used when gunicorn run)
    - create Procfile under the project and include "web: gunicorn run:app"
- To create runtime.txt
    - create runtime.txt under the project and include python version
- To login heroku
    - heroku login
- To create app on heroku
    - heroku create {appname}
- Add addon for postgresql
    - heroku addons:create heroku-postgresql:hobby-dev
- To update database URI for postgres on Heroku
    - SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
- To commit on git (example)
    - git add .
    - git commit
- To push to Heroku
    - git push heroku master
    *Remove some modules on requirements.txt if you face some issues during the installation on heroku
- To use email 
    - heroku config:set MAIL_USERNAME={your username}
    - heroku config:set MAIL_PASSWORD={your password}