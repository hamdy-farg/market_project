from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User
class RegisterForm(FlaskForm):
    def validate_user_name(self, user_name_to_check):
        user = User.query.filter_by(user_name=user_name_to_check.data).first()

        if user:
            raise ValidationError('Username already exist! Please try different username')
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exist try different email address ')  

    user_name = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    #?
    email_address = StringField(label='Email Addresss:', validators=[Email(), DataRequired()])
    #?
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    #?
    password2 = PasswordField(label= 'Confirm Password',validators=[EqualTo('password1'), DataRequired()])
    #?
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):

    email_address = StringField(label='Email Address')
    password = PasswordField(label='Password')
    submit = SubmitField(label= 'Login')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')