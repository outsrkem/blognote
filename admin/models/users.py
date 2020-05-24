from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time, random

dbsession, md, DBase = dbconnect()


class Users(DBase):
    __table__ = Table('users', md, autoload=True)
