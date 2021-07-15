from app.models import User

def signup(name, email, password):
    try:
        user = User(name, email)
        user.set_password(password)
        return user.to_dict()
    except:
        return None