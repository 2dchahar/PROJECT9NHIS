import bcrypt

USERS = {
    "admin": bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
}

def authenticate(username, password):
    if username in USERS:
        return bcrypt.checkpw(password.encode(), USERS[username])
    return False
