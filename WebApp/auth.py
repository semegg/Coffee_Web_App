from flask import flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user

from models import Admin

login_manager = LoginManager()
login_manager.login_view = '/login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.filter_by(id=user_id).first()


# Функція для входу користувача
def login(username, password):
    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        login_user(admin)
        admin.update_last_login(admin)
        flash('Logged in successfully', 'success')
        return True
    else:
        flash('Login failed. Check your username and password.', 'error')
        return False


# Функція для виходу користувача
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
