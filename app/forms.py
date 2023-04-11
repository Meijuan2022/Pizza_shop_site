from flask_wtf import FlaskForm, RecaptchaField, CSRFProtect
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, TelField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import *
from flask_wtf.file import FileField,FileRequired
from werkzeug.utils import secure_filename

from models import User


class User_PayForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=3, max=20)], default='Meijuan')
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=3, max=20)], default='Xia')
    address = StringField('Address', validators=[DataRequired(), Length(min=8, max=80)], default='sdfadfadfad152')
    phone = TelField('Telephone', validators=[DataRequired()], default='12345678')
    city = SelectField(
        choices=[('stockholm', 'Stockholm'), ('solna', 'Solna'), ('nacka', 'Nacka'), ('soluntuan', 'Soluntuan')])
    zip = StringField('Zip Code', validators=[DataRequired(), Length(min=8, max=10)], default='12345678')
    same_add = BooleanField('Shipping address is the same as my billing address')
    save_info = BooleanField('Save this information for next time')
    payment = RadioField(choices=[('card', 'Card'), ('paypal', 'PayPal'), ('swish', 'Swish')],
                         validators=[DataRequired()], default='card')
    namecard = StringField('Name on card', validators=[DataRequired(), Length(min=3, max=20)], default='Meijuan')
    cardnumber = StringField('Credit card number', validators=[DataRequired(), Length(min=3, max=20)],
                             default='1234567896547897')
    expi = StringField('Expiration', validators=[DataRequired(), Length(min=3, max=20)], default='01/28')
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=20)], default='123')
    submit = SubmitField('Continue to checkout')


class User_RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #    recaptcha = RecaptchaField()
    accept_tos = BooleanField('I accept the TOS', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username has already been taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email has already been taken!')


class User_LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    remember= BooleanField('Remember me')
    submit = SubmitField('Sign in')


class Admin_LoginForm(FlaskForm):
    manager = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=20)])
    submit = SubmitField('Sign in')

class Action_PizzaForm(FlaskForm):
    pizzaname = StringField("Pizza's name",validators=[DataRequired(), Length(min=1, max=20)])
    pizzapicture = FileField()
    #pizzapicture = FileField(validators=[FileRequired()])
    pizzaprice = FloatField('Price', validators=[DataRequired()])
    pizzasize = StringField("Pizza's size",validators=[DataRequired(), Length(min=1, max=5)])
    pizzatoppings = TextAreaField('Toppings', validators=[DataRequired()])
    pizzainventory =IntegerField('Inventory')
    submit = SubmitField('Submit')