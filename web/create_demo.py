from flask_user import SQLAlchemyAdapter, UserManager
from model import db, app, User, Role

if __name__ == '__main__':
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app)
    db.create_all()
    demo = User(username='demo', password=user_manager.hash_password('demo'), active=True)
    role = Role(name='user')
    demo.roles.append(role)
    db.session.add(demo)
    db.session.commit()