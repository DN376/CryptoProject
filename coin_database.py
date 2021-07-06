import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql.sqltypes import Float
from coin import Coin

Base = declarative_base()

class Coins(Base):
    __tablename__ = 'coin'
    name = Column(String(80))
    symbol = Column(String(10), nullable = False)
    price = Column(Float)
    marketCap = Column(Float)
    id = Column(Integer, primary_key=True)



engine = create_engine('sqlite:///coins_db.db')
Base.metadata.create_all(engine)