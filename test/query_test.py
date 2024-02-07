import unittest

import shell

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app = shell.app
        app.config['TESTING'] = True

        self.app = app.test_client()

        self.pl_code = '3950nyny'
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


    def test_join_query(self):
        response = self.app.get('/join?username=pmart0260&code=3950nyny')

        self.assertEqual(response.status_code, 200)
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
