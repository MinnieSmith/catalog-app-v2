from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask import Flask
from flask_login import LoginManager, UserMixin, AnonymousUserMixin
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
Base = declarative_base()
engine = create_engine('sqlite:///drugcatalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=True)


class OAuth(Base, OAuthConsumerMixin):
    user_id = Column(Integer, ForeignKey('user.id'))
    provider_user_id = Column(String(256), unique=True)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    user = relationship(User)


class DrugClass(Base):
    __tablename__ = 'drug_class'

    name = Column(String(250), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Drug(Base):
    __tablename__ = 'drug'

    name = Column(String(80), nullable=False, primary_key=True)
    drug_class_name = Column(String(80), ForeignKey('drug_class.name'))
    drug_class = relationship(DrugClass)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    information = Column(String, nullable=True)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }


class NewDrugs(Base):
    __tablename__ = 'new_drugs'

    name = Column(String(80), nullable=False, primary_key=True, unique=True)
    drug_class = Column(String, nullable=False)
    information = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'information': self.information,
            'id': self.id,
        }


engine = create_engine('sqlite:///drugcatalog.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)

