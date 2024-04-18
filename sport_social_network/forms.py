from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired


class SignInForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Войти')


class SignUpForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class PersonSettingsForm(FlaskForm):
    name = StringField('name')
    last_name = StringField('last_name')
    date_of_birth = StringField('date_of_birth')
    country = StringField('country')
    city = StringField('city')
    submit = SubmitField('Сохранить изменения')


class SportObjectSettingsForm(FlaskForm):
    name = StringField('name')
    country = StringField('country')
    city = StringField('city')
    address = StringField('address')
    phone = StringField('phone')
    submit = SubmitField('Сохранить изменения')
