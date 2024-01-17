
from sqlalchemy import Integer, String, JSON, Column
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column

from shell import db


class PickList(db.Model):
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True)
    code: Mapped[str] = mapped_column("code", String(12), nullable=False, unique=True)
    creator: Mapped[str] = mapped_column("creator", String(12), nullable=False, unique=True)

    usernames = mapped_column("users", ARRAY(db.String), nullable=False, unique=True, default=[])
    bins = Column("bins", MutableDict.as_mutable(JSONB), nullable=False, unique=True, default='[{{}}]')

    def __repr__(self):
        return '<Code %r users %s>' % (self.code, self.usernames)