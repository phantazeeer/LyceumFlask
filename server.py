import os

import flask_login
from flask import Flask, render_template, redirect
from werkzeug.utils import secure_filename

from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user
from data.users import User
from data.news import News
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.post_add import Add_Post
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
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.rep_pass.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            hashed_pass=form.password.data,
            name=form.name.data,
            surname=form.surname.data,
            birth=form.age.data,
            sec_name=form.second_name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = Add_Post()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        last_post = db_sess.query(News.id).all()[-1][0]
        print(form.pic.data)
        if form.pic.data:
            os.mkdir(f"static/posts_img/{last_post + 1}")
            for f in form.pic.data:
                file_name = secure_filename(f.filename)
                f.save(os.path.join(f"static/posts_img/{last_post + 1}", file_name))
                print(f"{file_name} добавлен")
        post = News(
            user_id=flask_login.current_user.id,
            post_named=form.name.data,
            text=form.text.data
        )
        db_sess.add(post)
        db_sess.commit()
        return 'пост успешно добавлен'
    return render_template("create_post.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/main")


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.run()