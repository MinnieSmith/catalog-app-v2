from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    # picture = Column(String(250), nullable=True)


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