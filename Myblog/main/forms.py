from flask_wtf import FlaskForm
from wtforms import StringField ,BooleanField,PasswordField , SubmitField
from Myblog.validators import DataRequired ,Length, Email, EqualTo , ValidationError
from Myblog.models import User


class RegisterationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=3,max=15)])
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('sign up')

    def Validate_username(self,username):
        user = User.query.filter_by(username=username.data).first() 
        if user:
            raise ValidationError('The username is already taken.')

    def Validate_username(self,email):
        user = User.query.filter_by(email=email.data).first() 
        if user:
            raise ValidationError('The email is already registered')

class LoginForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('log in')
