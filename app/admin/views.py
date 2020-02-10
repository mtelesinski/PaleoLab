from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import EditEmployeeForm
from ..auth import forms
from .. import db
from ..models import Employee


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Employee Views


@admin.route('/employees', methods=['GET', 'POST'])
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()

    return render_template('admin/employees/employees.html',
                           employees=employees, title="Employees")


@admin.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Add an employee to the database
    """
    check_admin()

    add_employee = True

    form = forms.RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password_hash=form.password.data)
        try:
            # add employee to the database
            db.session.add(employee)
            db.session.commit()
            flash('You have successfully added a new employee.')
        except:
            # in case employee e-mail already exists
            flash('Error: employee with this e-mail already exists.')

        # redirect to employees page
        return redirect(url_for('admin.list_employees'))

    # load employee template
    return render_template('admin/employees/employee.html', action="Add",
                           add_employee=add_employee, form=form,
                           title="Add Employee")


@admin.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    """
    Edit an employee
    """
    check_admin()

    add_employee = False

    employee = Employee.query.get_or_404(id)
    form = EditEmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.email = form.email.data
        employee.username = form.username.data
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        db.session.commit()
        flash('You have successfully edited the employee\'s data.')

        # redirect to the employees page
        return redirect(url_for('admin.list_employees'))

    form.email.data = employee.email
    form.username.data = employee.username
    form.first_name.data = employee.first_name
    form.last_name.data = employee.last_name
    return render_template('admin/employees/employee.html', action="Edit",
                           add_employee=add_employee, form=form,
                           employee=employee, title="Edit Employee's Data")


@admin.route('/employees/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete an employee from the database
    """
    check_admin()

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the employee.')

    # redirect to the employees page
    return redirect(url_for('admin.list_employees'))

    return render_template(title="Delete Employee")