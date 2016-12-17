# project/ test_main.py
import os
import unittest

from project import app, db

from project._config import basedir
from project.models import User


TEST_DB = 'test.db'

class MainTests(unittest.TestCase):

    ######################
    # setup and teardown #
    ######################

    # executed prior each test

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + \
            os.path.join(basedir, TEST_DB)
        # mockup client
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ##################
    # helper methods #
    ##################

    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)

    #########
    # tests #
    #########

    def test_404_error(self):
        response = self.app.get('/this-route-does-not-exists',
                                follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        # it's a good practice to not only check the status code.
        # but some text on the rendered HTML as well.
        # in the case of the 404 error, we have no idea what
        # the users sess on their end
        self.assertIn(b'Sorry. There\'s nothing here.', response.data)

    # def test_500_error(self):
    #     bad_user = User(
    #         name='Jeremy',
    #         email='jeremy@realpython.com',
    #         password='django'
    #     )
    #     db.session.add(bad_user)
    #     db.session.commit()
    #     response = self.login('Jeremy', 'django')
    #     self.assertEquals(response.status_code, 500)
    #     self.assertNotIn(b'ValueError: Invalid salt', response.data)
    #     self.assertIn(b'Something went terrible wrong.', response.data)

if __name__ == '__main__':
    unittest.main()
