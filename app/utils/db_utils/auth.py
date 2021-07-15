from app.models import User
from app import db

def signup(name, email, password):
    try:
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()
    except:
        return None

def signin(email, password):
    try:
        user: User = User.query.filter_by(email=email).first()
        if not user:
            return
        else:
            if user.check_password(password):
                return user.to_dict()
            return
    except:
        return None
