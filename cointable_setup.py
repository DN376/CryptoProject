import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Coin(Base):
    __tablename__ = 'coin'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    value = Column(String(8))
    prev_value = Column(String(8))
    perc_diff = Column(String(6))
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'value' : self.value,
            'prev_value' :self.prev_value,
            'perc_diff' : self.perc_diff
        }


engine = create_engine('sqlite:///cointable.db')


Base.metadata.create_all(engine)