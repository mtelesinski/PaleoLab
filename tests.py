# third-party imports
# import os
import unittest

from flask import abort, url_for
from flask_testing import TestCase

# local imports
from app import create_app, db
from app.models import Employee, Core


class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='postgresql://pl_admin:pl2019@localhost/paleolab_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Employee(username="admin", password="admin2016", is_admin=True)

        # create test non-admin user
        employee = Employee(username="test_user", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()





if __name__ == '__main__':
    unittest.main()
