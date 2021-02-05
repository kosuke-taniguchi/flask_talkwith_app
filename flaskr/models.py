from flaskr import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(), unique=True, index=True)
    password = db.Column(db.String(64))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def select_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class CreatePage(db.Model):

    __tablename__ = 'createpages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True)
    content = db.Column(db.String(128), index=True)
    time = db.Column(db.String(100))
    posts = db.relationship('Post', backref='createpages')

    def __init__(self, title, content, time):
        self.title = title
        self.content = content
        self.time = time.strftime('%Y年%m月%d日 %H:%M:%S')

    def add_page(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), index=True)
    username = db.Column(db.String(64), index=True)
    time = db.Column(db.String(100))
    page_id = db.Column(db.Integer, db.ForeignKey('createpages.id'))

    def __init__(self, content, username, time, page_id):
        self.content = content
        self.username = username
        self.time = time.strftime('%Y年%m月%d日 %H:%M:%S')
        self.page_id = page_id

    def add_post(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()