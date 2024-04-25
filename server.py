import os
import shutil

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
from forms.ref_prof import Refactor_Profile
import datetime
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
    if flask_login.current_user.is_authenticated:
        return redirect("/main")
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
        return redirect("/main")
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/main")
def main():
    db = db_session.create_session()
    s = db.query(News).all()
    date = datetime.datetime.now()
    return render_template("main.html", newslist=s, date=date)


@app.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():
    form = Add_Post()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        try:
            last_post = db_sess.query(News.id).all()[-1][0]
        except Exception:
            print("создание первого поста")
            last_post = 1
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
        return redirect("/main")
    return render_template("create_post.html", form=form)


@app.route("/profile/<int:profile>")
def profile(profile):
    db = db_session.create_session()
    info = db.query(User).filter(User.id == profile).first()
    return render_template("profile.html", info=info)


@app.route("/profile_refactor", methods=['GET', 'POST'])
@login_required
def profile_refactor():
    form = Refactor_Profile()
    db = db_session.create_session()
    worker = db.query(User).filter(User.id == flask_login.current_user.id).first()
    if form.validate_on_submit():
        worker.name = form.name.data
        worker.surname = form.surname.data
        worker.sec_name = form.second_name.data
        worker.country = form.country.data
        worker.city = form.city.data
        worker.projects = form.projects.data
        if form.picture.data:
            id_user = flask_login.current_user.id
            f = form.picture.data
            try:
                os.mkdir(f"static/profile_img/{id_user}")
            except Exception:
                shutil.rmtree(f"static/profile_img/{id_user}")
            try:
                os.mkdir(f"static/profile_img/{id_user}")
            except Exception:
                print("Не удалось создать папку")
            file_name = secure_filename(f.filename)
            f.save(os.path.join(f"static/profile_img/{id_user}", file_name))
            print(f"{file_name} добавлен")
        db.commit()
        return redirect(f"/profile/{flask_login.current_user.id}")
    else:
        form.name.data = worker.name
        form.surname.data = worker.surname
        form.second_name.data = worker.sec_name
        form.country.data = worker.country
        form.city.data = worker.city
        form.projects.data = worker.projects
    return render_template("ref_prof.html", form=form)


@app.route("/news_refactor/<int:post>", methods=['GET', 'POST'])
@login_required
def news_refactor(post):
    form = Add_Post()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == post).first()
    if form.validate_on_submit():
        if form.pic.data:
            try:
                os.mkdir(f"static/posts_img/{post}")
            except Exception:
                shutil.rmtree(f"static/posts_img/{post}")
            try:
                os.mkdir(f"static/posts_img/{post}")
            except Exception:
                print("не удалось создать папку")
            for f in form.pic.data:
                file_name = secure_filename(f.filename)
                f.save(os.path.join(f"static/posts_img/{post}", file_name))
                print(f"{file_name} добавлен")
        news.post_named = form.name.data
        news.text = form.text.data
        db_sess.commit()
        return redirect("/main")
    else:
        form.name.data = news.post_named
        form.text.data = news.text
    return render_template("create_post.html", form=form, page_name="Редактирование поста")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/main")


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.run()