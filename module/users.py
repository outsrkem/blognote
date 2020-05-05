from sqlalchemy import Table
from common.database import dbconnect

dbsession, md ,DBase = dbconnect()
class Users(DBase):
    __table__ = Table('users', md , autoload=True)

