from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask import Flask
from flask_login import LoginManager, UserMixin


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


# @login_manager.user_loader
# def load_user(user_id):
#     user = session.query(User).filter_by(id=user_id).first()
#     if user is not None:
#         return user
#     else:
#         return None


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class DrugClass(Base):
    __tablename__ = 'drug_class'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
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

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    drug_class_id = Column(Integer, ForeignKey('drug_class.id'))
    drug_class = relationship(DrugClass)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id
        }

class DrugInformation(Base):
    __tablename__ = 'drug_info'

    name = Column(String(80), nullable=False, primary_key=True)
    information = Column(String, nullable=True)
    drug_class_id = Column(Integer, ForeignKey('drug_class.id'))
    drug_class = relationship(DrugClass)
    drug_id = Column(Integer, ForeignKey('drug.id'))
    drug = relationship(Drug)
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


class NewDrugs(Base):
    __tablename__ = 'new_drugs'

    name = Column(String(80), nullable=False)
    information = Column(String, nullable=True)
    id = Column(Integer, primary_key=True)
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

class NewDrugInformation(Base):
    __tablename__ = 'new_drug_info'

    name = Column(String(80), nullable=False, primary_key=True)
    information = Column(String, nullable=True)
    new_drugs_id = Column(Integer, ForeignKey('new_drugs.id'))
    new_drug = relationship(NewDrugs)
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


engine = create_engine('sqlite:///drugcatalog.db')


Base.metadata.create_all(engine)