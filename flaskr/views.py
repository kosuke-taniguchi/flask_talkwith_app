from flask import Blueprint, render_template, request, redirect, url_for, flash
from flaskr.forms import LoginForm, RegisterForm, CreatePageForm, PostForm
from flaskr.models import User, CreatePage, Post
from flask_login import login_user, logout_user, login_required
import datetime


bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/welcome')
@login_required
def user_page():
    create_page = CreatePage.query.all()
    return render_template('user_page.html', create_page=create_page)

@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        user = User.select_user_by_email(email)
        if user and user.validate_password(password):
            login_user(user)
            next = request.args.get('next')
            if not next:
                next = url_for('app.user_page')
            flash('ログインしました！')
            return redirect(next)
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(
            username,
            email,
            password
        )
        user.add_user()
        flash('登録が完了しました。ご利用するにはログインしてください。')
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)

@bp.route('/createpage', methods=['POST', 'GET'])
@login_required
def create_page():
    form = CreatePageForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        content = form.content.data
        time = datetime.datetime.now()
        create_page = CreatePage(
            title,
            content,
            time
        )
        create_page.add_page()
        flash('新しいトピックのページを作成しました！')
        return redirect(url_for('app.user_page'))
    return render_template('create_page.html', form=form)

@bp.route('/go_to_see/<int:page_id>')
@login_required
def go_to_see(page_id):
    # page = CreatePage.query.get(page_id)
    # posts = Post.query.filter(page).all()
    # posts = page.posts.query.all()
    # posts = page.posts
    # posts = Post.query.filter(Post.page_id==CreatePage.id).all()
    page_id = page_id
    posts = Post.query.filter(Post.page_id == page_id).all()
    return render_template('go_to_see.html', page_id=page_id, posts=posts)

@bp.route('/post/<int:page_id>', methods=['GET', 'POST'])
@login_required
def post(page_id):
    form = PostForm(request.form)
    page_id = page_id
    if request.method == 'POST' and form.validate():
        content = form.content.data
        username = form.username.data
        page_id = form.page_id.data
        time = datetime.datetime.now()
        post = Post(
            content,
            username,
            time,
            page_id
        )
        post.add_post()
        flash('新しく投稿しました！')
        return redirect(url_for('app.user_page'))
    return render_template('post.html', form=form, page_id=page_id)