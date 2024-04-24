from flask import Flask, render_template
from data import db_session
from flask_login import LoginManager
from data.users import User
from forms.login_form import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form, title='Авторизация')


@app.route("/register")
def register():
    return None


@app.route("/main")
def main():
    return render_template("main.html")


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.run()