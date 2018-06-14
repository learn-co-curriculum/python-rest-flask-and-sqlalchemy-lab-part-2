import os, unittest, tempfile, sys, json
sys.path.insert(0, '..')
from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_users_index(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertTrue('<h3>Username: Jeff</h3>' in raw)
        self.assertTrue('<h3>Username: Rachel</h3>' in raw)
        self.assertTrue('<h3>Username: Daniel</h3>' in raw)

    def test_user_by_id(self):
        response = self.app.get('/users/3')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertTrue('<h3>Username: Daniel</h3>' in raw)
        self.assertTrue('<p>ID: 3</p>' in raw)
        self.assertTrue('<p>Content: I love hogs</p>' in raw)
        self.assertTrue('<p>Content: Hogs are the best way to teach react</p>' in raw)
        self.assertTrue('<p>Content: Programming is lyfe</p>' in raw)

    def test_user_by_name(self):
        response = self.app.get('/users/daniel')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertTrue('<h3>Username: Daniel</h3>' in raw)
        self.assertTrue('<p>ID: 3</p>' in raw)
        self.assertTrue('<p>Content: I love hogs</p>' in raw)
        self.assertTrue('<p>Content: Hogs are the best way to teach react</p>' in raw)
        self.assertTrue('<p>Content: Programming is lyfe</p>' in raw)

    def test_tweets_index(self):
        response = self.app.get('/tweets')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertEqual(raw.count("<h4>Author: Jeff</h4>"), 3)
        self.assertEqual(raw.count("<h4>Author: Rachel</h4>"), 3)
        self.assertEqual(raw.count("<h4>Author: Daniel</h4>"), 3)
        self.assertEqual(raw.count("Author:"), 9)
        self.assertEqual(raw.count("Content:"), 9)

    def test_tweets_by_id(self):
        response = self.app.get('/tweets/1')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertTrue('<h3>Author: Jeff</h3>' in raw)
        self.assertTrue('<p>Content: Data Science is awesome</p>' in raw)
        self.assertTrue('<p>User ID: 1</p>' in raw)

    def test_user_by_id_tweets(self):
        response = self.app.get('/users/2/tweets')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertEqual(raw.count('<h4>Author: Rachel</h4>'), 3)
        self.assertTrue('<p>Content: RPDR is the best show</p>' in raw)
        self.assertTrue('<p>Content: I just made the coolest NPM package!</p>' in raw)
        self.assertTrue('<p>Content: Running is so fun!</p>' in raw)

    def test_user_by_name_tweets(self):
        response = self.app.get('/users/rachel/tweets')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertEqual(raw.count('<h4>Author: Rachel</h4>'), 3)
        self.assertTrue('<p>Content: RPDR is the best show</p>' in raw)
        self.assertTrue('<p>Content: I just made the coolest NPM package!</p>' in raw)
        self.assertTrue('<p>Content: Running is so fun!</p>' in raw)

    def test_tweets_by_id_user(self):
        response = self.app.get('/tweets/7/user')
        self.assertEqual(response.status_code, 200)
        raw = response.data.decode("utf-8")
        self.assertTrue('<h3>Username: Daniel</h3>' in raw)
        self.assertTrue('<p>ID: 3</p>' in raw)
        self.assertTrue('<p>Content: I love hogs</p>' in raw)
        self.assertTrue('<p>Content: Hogs are the best way to teach react</p>' in raw)
        self.assertTrue('<p>Content: Programming is lyfe</p>' in raw)


if __name__ == '__main__':
    unittest.main()
