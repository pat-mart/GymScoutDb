import sqlalchemy.exc
from sqlalchemy.orm.attributes import flag_modified

from pick_list import PickList
from shell import db


class Manager:

    @staticmethod
    def is_username_free(username: str, code: str) -> bool:

        pl = Manager.get_pick_list(code)

        return username not in pl.usernames and pl.creator != username

    @staticmethod
    def clear_table():
        query = db.session.query(PickList)

        try:
            query.delete()
        except sqlalchemy.exc.ProgrammingError:
            return

        db.session.commit()

    @staticmethod
    def add_user(code: str, username: str):

        if not Manager.is_username_free(username, code):
            return

        entry = db.session.query(PickList).filter_by(code=code).first()

        entry.usernames.append(username)

        flag_modified(entry, 'usernames')

        db.session.commit()

    @staticmethod
    def user_leave(code: str, username: str):
        entry = Manager.get_pick_list(code)
        usernames = entry.usernames

        if username not in usernames:
            return

        usernames.remove(username)

        flag_modified(entry, 'usernames')

        db.session.commit()

    @staticmethod
    def add_list(new_item: PickList):
        db.session.add(new_item)
        db.session.commit()

    @staticmethod
    def get_pick_list(passcode: str) -> PickList:
        return db.session.query(PickList).filter_by(code=passcode).first()

    @staticmethod  # Managing such a feature in a user app would be difficult. Not sure if would be useful
    def edit_entry(passcode: str, new_vers: PickList):
        pl = Manager.get_pick_list(passcode)

        if pl:
            pl.update(new_vers)
            db.session.commit()

    @staticmethod
    def add_bin(passcode: str, bin_category: str, bin_value: int, team_num: int):
        bins = Manager.get_pick_list(passcode).bins

        if team_num in bins:
            bins[team_num][bin_category] = bin_value

        flag_modified(bins, "bins")

        db.session.commit()

    @staticmethod
    def edit_bin_value(passcode: str, bin_category: str, bin_value: int, team_num: int):
        bins = Manager.get_pick_list(passcode).bins

        if not bins or not bins[team_num]:
            return

        bins[team_num][bin_category] = bin_value
        db.session.commit()

    @staticmethod
    def delete_entry(passcode: str, username: str):
        pl = Manager.get_pick_list(passcode)

        if pl and username == pl.creator:
            db.session.delete(pl)
            db.session.commit()
