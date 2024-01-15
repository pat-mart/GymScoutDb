from sqlalchemy import Integer, String, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from shell import db


class PickList(db.Model):
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    code: Mapped[str] = mapped_column("code", String(12), nullable=False, unique=True)
    creator: Mapped[str] = mapped_column("creator", String(12), nullable=False, unique=True)

    usernames = mapped_column("users", ARRAY(db.String), nullable=True, unique=True, default=[])
    bins = mapped_column("bins", JSON, nullable=False, unique=True)

    def __repr__(self):
        return '<Code %r>' % self.code