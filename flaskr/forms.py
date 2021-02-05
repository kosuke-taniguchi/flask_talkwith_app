from wtforms import Form
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields import StringField, PasswordField, TextAreaField, SubmitField, HiddenField


class LoginForm(Form):
    email = StringField('メールアドレス: ', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード: ', validators=[DataRequired()])
    submit = SubmitField('ログイン')


class RegisterForm(Form):
    username = StringField('ユーザー名: ', validators=[DataRequired()])
    email = StringField('メールアドレス: ', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード: ', validators=[DataRequired(), EqualTo('confirm_password', message='パスワードが一致しません')])
    confirm_password = PasswordField('パスワードの確認: ', validators=[DataRequired()])
    submit = SubmitField('登録')


class CreatePageForm(Form):
    title = StringField('タイトル: ', validators=[DataRequired()])
    content = TextAreaField('内容: ', validators=[DataRequired()])
    submit = SubmitField('新規ページ作成: ', validators=[DataRequired()])


class PostForm(Form):
    content = TextAreaField('内容: ', validators=[DataRequired()])
    username = HiddenField('', validators=[DataRequired()])
    page_id = HiddenField('', validators=[DataRequired()])
    submit = SubmitField('投稿')