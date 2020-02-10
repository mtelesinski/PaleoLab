from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DecimalField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CoreForm(FlaskForm):
    """
    Form for users to add new cores
    """
    name = StringField('Name', validators=[DataRequired()])
    lat = DecimalField('Latitude (in 000.00000 format, southern latitudes as negative numbers)', places=5)
    lon = DecimalField('Longitude (in 000.00000 format, western longitudes as negative numbers)', places=5)
    w_depth_m = IntegerField('Water depth (in m)')
    length_cm = IntegerField('Core length (in cm)')
    type = StringField('Core type')
    submit = SubmitField('Add')
