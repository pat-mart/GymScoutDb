from pick_list import PickList
from shell import db


class Manager:

    @staticmethod
    def add_user(code: str, username: str):
        entry = db.session.query(PickList).filter(PickList.code == code)
        entry.append(username)

        db.session.commit()

    @staticmethod
    def add_list(new_item: PickList):
        db.session.add(new_item)
        db.session.commit()

    @staticmethod
    def get_pick_list(passcode: str) -> PickList:
        return db.session.query(PickList).filter_by(code=passcode).first()

    @staticmethod
    def edit_entry(passcode: str, new_vers: PickList):
        pl = Manager.get_pick_list(passcode)

        if pl:
            pl.update(new_vers)
            db.session.commit()

    @staticmethod
    def delete_entry(passcode: str):
        pl = Manager.get_pick_list(passcode)

        if pl:
            db.session.delete(pl)
            db.session.commit()
