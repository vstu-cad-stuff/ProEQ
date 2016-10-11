from model import db, app, User, Role, user_manager

if __name__ == '__main__':
    db.create_all()
    demo = User(username='demo', password=user_manager.hash_password('demo'), active=True)
    role = Role(name='user')
    demo.roles.append(role)
    db.session.add(demo)
    db.session.commit()