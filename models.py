from sqlalchemy import create_engine, Column, Date, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)
    brand_id = Column(Integer, ForeignKey('brands.brand_id'))