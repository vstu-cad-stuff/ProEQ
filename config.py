from os import path

PROJECT_DIRECTORY = path.dirname(__file__)
UPLOAD_FOLDER = path.join(PROJECT_DIRECTORY, 'upload')
SQLALCHEMY_DATABASE_URI = 'sqlite:////' + path.join(PROJECT_DIRECTORY, 'database.db')
SECRET_KEY = 'pro-eq-secret-project-key'