from main import app
import unittest

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_get_message(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/message')

        self.assertEqual(result.status_code, 200)

        # assert the response data
        self.assertEqual(result.data, b'Hello Stonks')


if __name__ == '__main__':
    unittest.main()
