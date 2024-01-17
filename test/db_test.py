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
            bins={3950: {"max_points": 0}, 254: {"auto_points": 25}}
        )

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
            Manager.add_user("3950nyny", "rico")
            Manager.add_user("3950nyny", "loo_mart")

            self.assertEqual(len(pl.usernames), 3)

            Manager.user_leave("3950nyny", "p_mart")
            Manager.user_leave("3950nyny", "rico")
            Manager.user_leave("3950nyny", "loo_mart")

            self.assertEqual(len(pl.usernames), 0)

    def test_creates_pl(self):
        with app.app_context():
            Manager.clear_table()

            new_val = PickList(
                code="hello_world",
                creator="pat-mart",
                usernames=[],
                bins={"max_points": 0, "auto_points": 0, "teleop_points": 0}
            )

            Manager.add_list(new_val)

            pl = Manager.get_pick_list("hello_world")

            self.assertIsNotNone(pl, "PickList was not created")


if __name__ == '__main__':
    unittest.main()
