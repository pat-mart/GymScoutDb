import random
import string
import unittest

from manager import Manager
from pick_list import PickList
from shell import app, db


class DbTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.init_app(app)
        app.config['TESTING'] = True

    @staticmethod
    def get_pl(code) -> PickList:
        return PickList(
            code=code,
            creator="pat-mart",
            usernames=[],
            bin_keys=["hello", "goodbye"],
            bins={}
        )

    def test_invalid_username(self):
        with app.app_context():
            Manager.clear_table()

            Manager.add_list(DbTest.get_pl('aefwe3950'))
            Manager.add_user('aefwe3950', 'pat-mart')

            Manager.add_user('aefwe3950', 'hello_man')
            Manager.add_user('aefwe3950', 'hello_man')

            self.assertEqual(len(Manager.get_pick_list('aefwe3950').usernames), 1)

    def test_joins_pl(self):
        with app.app_context():
            Manager.clear_table()

            Manager.add_list(DbTest.get_pl("3950nyny"))

            for i in range(100):
                random_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
                Manager.add_user("3950nyny", random_str)

            pl = Manager.get_pick_list("3950nyny")

            self.assertEqual(len(pl.usernames), 100)

    def test_removes_user(self):
        with app.app_context():
            Manager.clear_table()

            Manager.add_list(DbTest.get_pl("3950nyny"))
            pl = Manager.get_pick_list("3950nyny")

            Manager.add_user("3950nyny", "p_mart")
            Manager.add_user("3950nyny", "j_mart")
            Manager.add_user("3950nyny", "loo_mart")

            self.assertEqual(len(pl.usernames), 3)

            Manager.user_leave("3950nyny", "p_mart")
            Manager.user_leave("3950nyny", "j_mart")
            Manager.user_leave("3950nyny", "loo_mart")

            self.assertEqual(len(pl.usernames), 0)

    def test_creates_pl(self):
        with app.app_context():

            db.create_all()

            Manager.clear_table()

            new_val = PickList(
                code='hello_world',
                creator="pat-mart",
                usernames=[],
                bins={},
                bin_keys=["auto_points", "teleop points", "auto game pieces"],
            )

            Manager.add_list(new_val)

            pl = Manager.get_pick_list("hello_world")

            self.assertIsNotNone(pl)


if __name__ == '__main__':
    unittest.main()
