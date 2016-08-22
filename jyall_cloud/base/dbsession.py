# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
#from zope.sqlalchemy import ZopeTransactionExtension
from jyall_cloud.config import get_mysql_config_url
import random



MASTER_SQLALCHEMY_CONF_URL = get_mysql_config_url(role='master')

SLAVE_SQLALCHEMY_CONF_URL = get_mysql_config_url(role='slave')

engines = {
    'leader': create_engine(
        MASTER_SQLALCHEMY_CONF_URL,logging_name='leader', echo=True),
    # 'other': create_engine(
        # SLAVE_SQLALCHEMY_CONF_URL,logging_name='other', echo=True),
    'follower': create_engine(
        MASTER_SQLALCHEMY_CONF_URL,logging_name='follower', echo=True),
    # 'follower2': create_engine(
    #     'sqlite:///follower2.db',
    #     logging_name='follower2', echo=True),
}

class RoutingSession(Session):

    def get_bind(self, mapper=None, clause=None):
        if self._name:
            return engines[self._name]
        elif self._flushing:
            return engines['leader']
        # elif mapper and issubclass(mapper.class_, MyOtherClass):
        #     return engines['other']
        else:
            return engines[
                random.choice(['follower'])]
    _name = None

    def using_bind(self, name):
        s = RoutingSession()
        vars(s).update(vars(self))
        s._name = name
        return s


Base = declarative_base()
#DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),class_=RoutingSession))
DBconf=MASTER_SQLALCHEMY_CONF_URL
engine = create_engine(DBconf)
session = sessionmaker(bind=engine)
DBSession=session()
def dbsession_generator():
    return DBSession()


