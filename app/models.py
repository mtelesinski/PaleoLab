from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Core(db.Model):
    """
    Create a Core table
    """

    __tablename__ = 'cores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    lat = db.Column(db.Numeric(8, 5))
    lon = db.Column(db.Numeric(8, 5))
    w_depth_m = db.Column(db.Integer)
    length_cm = db.Column(db.Integer)
    type = db.Column(db.String(10))
    # samples = db.relationship('Sample', backref='core',
    #                             lazy='dynamic')

    def __repr__(self):
        return '<Core: {}>'.format(self.name)


# TO BE USED LATER IN THE PROJECT #
# class Sample_stabiso(db.Model):
#     """
#     Create a Sample_stabiso table
#     """
#
#     __tablename__ = 'samples'
#
#     id = db.Column(db.Integer, primary_key=True)
#     depth_cm = db.Column(db.Numeric(precision=1))
#     age_ka = db.Column(db.Numeric(precision=3))
#     d13C = db.Column(db.Numeric(precision=3))
#     d18O = db.Column(db.Numeric(precision=3))
#
#     def __repr__(self):
#         return '<Sample: {}>'.format(self.name)
