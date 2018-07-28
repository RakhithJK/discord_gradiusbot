import traceback
import logging
from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///banpool_configuration.db')
Base.metadata.bind = engine
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()

# Setup Logging
logger = logging.getLogger('banpool_configuration')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('banpool_configuration.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


class BanpoolConfigManager:
    def build_db(self):
        Base.metadata.create_all(engine)

    def set_announce_chan(self, server_id, channel_id, author, author_id):
        try:
            now = datetime.now()
            target_server = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

            # the server exists, set its channel
            if target_server:
                target_server.announce_chan = channel_id
                session.add(target_server)
                session.commit()

            # the server doesn't exist, create it and set its channel
            else:
                new_server = BanpoolConfig(server_id=server_id, announce_chan=channel_id, last_edit_date=now,
                                           last_edit_author=author, last_edit_id=author_id)
                session.add(new_server)
                session.commit()

        except:
            logger.error(traceback.format_exc())

    def set_pool_level(self, server_id, pool_name, level, author, author_id):
        try:
            now = datetime.now()
            target_server = session.query(BanpoolConfig).filter(BanpoolConfig.server_id==server_id).first()

            if target_server:
                # TODO: Finish this.
                pass
            else:
                new_server = BanpoolConfig(server_id=server_id, last_edit_date=now, last_edit_author=author,
                                           last_edit_id=author_id)
                session.add(new_server)
                session.commit()

        except:
            logger.error(traceback.format_exc())


class BanpoolConfig(Base):
    __tablename__ = 'banpoolconfig'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    announce_chan = Column(String)
    last_edit_date = Column(DateTime)
    last_edit_author = Column(String)
    last_edit_id = Column(Integer)
    subscriptions = relationship('PoolSubscription')


class PoolSubscription(Base):
    __tablename__ = 'poolsubscription'
    id = Column(Integer, primary_key=True)
    banpool_config_id = Column(Integer, ForeignKey('banpoolconfig.id'))
    pool_name = Column(String)
    sub_type = Column(String)
