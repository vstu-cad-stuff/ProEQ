import os

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ['DEBUG']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_SERVICE = os.environ['DB_SERVICE']
DB_PORT = os.environ['DB_PORT']
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
)
PROJECT_DIRECTORY = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(PROJECT_DIRECTORY, 'upload')
USER_ENABLE_EMAIL = False
USER_ENABLE_LOGIN_WITHOUT_CONFIRM = True
USER_ENABLE_CONFIRM_EMAIL = False
USER_ENABLE_REGISTRATION = False
USER_APP_NAME = 'ProEQ'