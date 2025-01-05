from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])  # 允许上传的图片格式
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RateForm(FlaskForm):
    score = IntegerField('Score (0-100)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Submit')

class UploadAvatarForm(FlaskForm):
    avatar = FileField('上传头像', validators=[FileAllowed(['jpg', 'png', 'jpeg'], '仅支持 JPG, PNG, JPEG 格式')])
    submit = SubmitField('上传')

