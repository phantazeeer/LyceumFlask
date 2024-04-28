import os
import shutil

import flask_login
from flask import Flask, render_template, redirect
from werkzeug.utils import secure_filename

import user_resources
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user
from data.users import User
from data.news import News
from data.comments import Comment
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.post_add import Add_Post
from forms.add_comment import AddComment
from forms.ref_prof import Refactor_Profile
from forms.like import Like
from flask_restful import reqparse, abort, Api, Resource
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/liked_post/<int:id_post>")
def liked_post(id_post):
    db = db_session.create_session()
    user = db.query(User).filter(User.id == flask_login.current_user.id).first()
    post = db.query(News).filter(News.id == id_post).first()
    num = str(id_post)
    try:
        liked = user.liked_posts.split(";")
        if num in liked:
            post.likes -= 1
            liked.remove(num)
        else:
            post.likes += 1
            liked.append(num)
    except Exception:
        post.likes += 1
        liked = []
        liked.append(num)
    user.liked_posts = ";".join(liked)
    db.commit()
    return redirect("/main")


@app.route("/liked_comm/<int:id_comm>")
def liked_comm(id_comm):
    db = db_session.create_session()
    user = db.query(User).filter(User.id == flask_login.current_user.id).first()
    comm = db.query(Comment).filter(Comment.id == id_comm).first()
    num = str(id_comm)
    try:
        liked = user.liked_somments.split(";")
        if num in liked:
            comm.likes -= 1
            liked.remove(num)
        else:
            comm.likes += 1
            liked.append(num)
    except Exception:
        comm.likes += 1
        liked = []
        liked.append(num)
    user.liked_somments = ";".join(liked)
    db.commit()
    return redirect(f"/full_post/{comm.post_id}")


@app.route("/", methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
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
        posts = db_sess.query(News).all()
        if form.pic.data:
            for f in form.pic.data:
                file_name = secure_filename(f.filename)
                if file_name in [i.picture for i in db_sess.query(News.picture).all()]:
                    file_name = f"{posts[-1].id + 1}" + file_name
                f.save(os.path.join(f"static/posts_img", file_name))
                print(f"{file_name} добавлен")
                post = News(
                    user_id=flask_login.current_user.id,
                    post_named=form.name.data,
                    text=form.text.data,
                    picture=file_name
                )
        else:
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
    news = db.query(News).filter(News.user_id == profile).all()
    return render_template("profile.html", info=info, newslist=news)


@app.route("/full_post/<int:id_post>", methods=['GET', 'POST'])
def full_post(id_post):
    form = AddComment()
    db = db_session.create_session()
    item = db.query(News).filter(News.id == id_post).first()
    comments = db.query(Comment).filter(Comment.post_id == id_post).all()
    if form.validate_on_submit():
        if form.picture.data:
            for f in form.picture.data:
                file_name = secure_filename(f.filename)
                if file_name in [i.pic for i in db.query(Comment.pic).all()]:
                    file_name = f"{comments[-1].id}" + file_name
                f.save(os.path.join(f"static/comms_img", file_name))
                new_comm = Comment(
                    text=form.text.data,
                    user_id=flask_login.current_user.id,
                    post_id=id_post,
                    pic=file_name
                )
                print(f"{file_name} добавлен")
        else:
            new_comm = Comment(
                text=form.text.data,
                user_id=flask_login.current_user.id,
                post_id=id_post
            )
        db.add(new_comm)
        db.commit()
        return redirect(f"{id_post}")
    return render_template("post.html", comments=comments, item=item, form=form)


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
            f = form.picture.data
            file_name = secure_filename(f.filename)
            if file_name in [i.picture for i in db.query(User.picture).all()]:
                file_name = f"{worker.id}" + file_name
            f.save(os.path.join(f"static/profile_img", file_name))
            print(f"{file_name} добавлен")
            worker.picture = file_name
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
            for f in form.pic.data:
                file_name = secure_filename(f.filename)
                if file_name in [i.picture for i in db_sess.query(News.picture).all()]:
                    file_name = f"{news.id}" + file_name
                f.save(os.path.join(f"static/posts_img/{post}", file_name))
                news.picture = file_name
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
    # для списка объектов
    api.add_resource(user_resources.UserListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(user_resources.UserResource, '/api/v2/user/<int:user_id>')
    db_session.global_init("db/blogs.db")
    app.run()
#changes for commit