from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from ..auth import forms
from .. import db
from ..models import Employee, Core


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(
                form.password.data):
            # log employee in
            login_user(employee)

            # redirect to the appropriate dashboard page
            return redirect(url_for('auth.list_cores'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('home.homepage'))


# Core views

@auth.route('/cores', methods=['GET', 'POST'])
@login_required
def list_cores():
    """
    List all cores
    """
    cores = Core.query.all()

    return render_template('auth/cores/cores.html',
                           cores=cores, title="Cores")


@auth.route('/cores/add', methods=['GET', 'POST'])
@login_required
def add_core():
    """
    Add a core to the database
    """
    add_core = True

    form_c = forms.CoreForm()
    if form_c.validate_on_submit():
        core = Core(name=form_c.name.data,
                    lat=form_c.lat.data,
                    lon=form_c.lon.data,
                    w_depth_m=form_c.w_depth_m.data,
                    length_cm=form_c.length_cm.data,
                    type=form_c.type.data)
        try:
            # add core to the database
            db.session.add(core)
            db.session.commit()
            flash('You have successfully added a new core.')
        except:
            # in case core name already exists
            flash('Error: core with this name already exists.')

        # redirect to cores page
        return redirect(url_for('auth.list_cores'))

    # load core template
    return render_template('auth/cores/core.html', action="Add",
                           add_core=add_core, form_c=form_c,
                           title="Add Core")


@auth.route('/cores/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_core(id):
    """
    Edit a core
    """
    add_core = False

    core = Core.query.get_or_404(id)
    form_c = forms.CoreForm(obj=core)
    if form_c.validate_on_submit():
        core.name = form_c.name.data,
        core.lat = form_c.lat.data,
        core.lon = form_c.lon.data,
        core.w_depth_m = form_c.w_depth_m.data,
        core.length_cm = form_c.length_cm.data,
        core.type = form_c.type.data
        db.session.commit()
        flash('You have successfully edited the core\'s data.')

        # redirect to the core page
        return redirect(url_for('auth.list_cores'))

    form_c.name.data = core.name
    form_c.lat.data = core.lat
    form_c.lon.data = core.lon
    form_c.w_depth_m.data = core.w_depth_m
    form_c.length_cm.data = core.length_cm
    form_c.type.data = core.type
    return render_template('auth/cores/core.html', action="Edit",
                           add_core=add_core, form_c=form_c,
                           core=core, title="Edit Core's Data")


@auth.route('/cores/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_core(id):
    """
    Delete a core from the database
    """
    core = Core.query.get_or_404(id)
    db.session.delete(core)
    db.session.commit()
    flash('You have successfully deleted the core.')

    # redirect to the cores page
    return redirect(url_for('auth.list_cores'))

    return render_template(title="Delete Core")
