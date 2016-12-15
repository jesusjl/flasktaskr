import os
import unittest

from project import app, db
from project._config import basedir
from project.models import Task, User

TEST_DB = 'test.db'

class AllTest(unittest.TestCase):

    # Setup and teardown

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after each test_client
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password,
                      confirm=confirm),
            follow_redirects=True
        )

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_admin_user(self):
        new_user = User(
            name='Superman',
            email='admin@realpython',
            password='allpowerful',
            role='admin'
        )
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='02/05/2014',
            priority=1,
            posted_date='02/04/2014',
            status='1'
        ), follow_redirects=True)

    # each test should start with 'test'

    def test_user_can_register(self):
        new_user = User('Michael', 'michael@mherman.org',
                        'michaelherman')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
            assert t.name == 'Michael'

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your task list',
                      response.data)

    def test_welcome_message(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to FlaskTaskr.', response.data)

    def test_user_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)

    def test_user_can_login(self):
        self.register('Michael',
                      'michael@reappython.com',
                      'python',
                      'python')
        response = self.login('Michael', 'python')
        self.assertIn(b'Welcome to FlaskTaskr', response.data)

    def test_invalid_form_data(self):
        self.register('Michael', 'michael@realpython.com',
                      'python', 'python')
        response = self.login('alert("alert box!")', 'foo')
        self.assertIn(b'Invalid username or password', response.data)

    # test form is present on register page
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.',
                      response.data)

    # test that the actual form is preset rather than just some
    # other element on the same page as the form

    # def test_user_registration(self):
    #     self.app.get('register/', follow_redirects=True)
    #     response = self.register('Michael'
    #                              'michael@realpython',
    #                              'python',
    #                              'python')
    #     self.assertIn(b'Thanks for registering. Please login.',
    #                   response.data)

    # refactoring....
    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('Michael', 'michael@realpython.com',
                      'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = self.register('Michael', 'michael@realpython.com',
                                 'python', 'python')
        self.assertIn(b'That username and/or email already exist.',
                      response.data)

    def test_logged_in_user_can_logout(self):
        self.register('Michael', 'michael@realpython.com', 'python', 'python')
        self.login('Michael', 'python')
        response = self.logout()
        self.assertIn(b'Goodbye', response.data)

    def test_not_logged_in_user_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye', response.data)

    def test_logged_in_user_can_access_tasks_page(self):
        self.register('Fletcher', 'fletcher@realpython.com',
                      'python101', 'python101')
        response = self.login('Fletcher', 'python101')
        # response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_user_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    def test_default_user_role(self):

        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )

        db.session.commit()

        users = db.session.query(User).all()
        # print users
        for user in users:
            self.assertEquals(user.role, 'user')

    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertNotIn(
            b'You can only update task that belong to you',
            response.data
        )

    def tast_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user('Michael', 'michael@realpython.com', 'python')
        self.login('Michael', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman', 'allpowerful')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("delete/1", follow_redirects=True)
        self.assertNotIn(b'You can only delete tasks that belong to you',
                         response.data)
