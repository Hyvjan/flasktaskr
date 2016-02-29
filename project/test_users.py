import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

	#############################
	##### setup and teardown#####
	#############################

	def setUp(self):
		app.config['TESTING']=True
		app.config['WTF_CSRF_ENABLED']=False
		app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + \
			os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

	# executed after each test
	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# Helper function to log users in 
	def login(self, name, password):
		return self.app.post('/', data=dict(
			name=name, password=password), follow_redirects=True)

	#Helper function to register user
	def register(self, name, email, password, confirm):
		return self.app.post(
			'register/', data=dict(name=name, email=email, password=password,
				confirm=confirm),
			follow_redirects=True
			)

	# Get logout/ page 
	def logout(self):
		return self.app.get('logout/', follow_redirects=True)

	#helper function to create user
	def create_user(self, name, email, password):
		new_user = User(name=name, email=email, password=password)
		db.session.add(new_user)
		db.session.commit()

	def check_form_is_present(self, rout, assertText):
		response = self.app.get(rout)
		bitti=assertText.encode("utf-8")
		self.assertEqual(response.status_code, 200)
		self.assertIn(bitti,response.data)

	def test_user_can_register(self):
		self.create_user("michael", "michael@mherman.org",
			"michaelherman")
		test=db.session.query(User).all()
		for t in test:
			t.name
		assert t.name == "michael"

	def test_form_is_present_on_login_page(self):
		self.check_form_is_present('/', 'Please sign in to access your task list')

	def test_users_cannot_login_unless_registered(self):
		response=self.login('foo', 'bar')
		self.assertIn(b'Invalid username or password', response.data) 

	def test_users_can_login(self):
		self.register('Michael', 'michael@realpython.com', 'python', 
			'python')
		response=self.login('Michael', 'python')
		self.assertIn('Welcome!', response.data)

	def test_invalid_form_data(self):
		self.register('Michael', 'Michael@realpython.com', 'python',
			'python')
		response = self.login('alert("alert box!");', 'foo')
		self.assertIn(b'Invalid username or password.', response.data)



if __name__ == "__main__":
	unittest.main()