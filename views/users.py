from flask import Blueprint, render_template, request, session, redirect, url_for
from models.alert import Alert
from models.user import User, UserErrors


user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            User.register_user(email, password)
            session['email'] = email
            return redirect(url_for('alerts.index'))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.html")


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('alerts.index'))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.html")


@user_blueprint.route('/logout', methods=['GET', 'POST'])
def logout_user():
    session['email'] = None
    return redirect(".login_user")
