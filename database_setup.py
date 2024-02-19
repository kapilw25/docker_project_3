# Create an SQLite database and design tables to store user engagement data.


from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = 'sqlite:///online_retail.db'

Base = declarative_base()

class RetailData(Base):
    __tablename__ = 'retail_data'
    id = Column(Integer, primary_key=True, index=True)
    invoice = Column(String, index=True)
    stock_code = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    invoice_date = Column(DateTime)
    price = Column(Float)
    customer_id = Column(Integer, index = True)
    country = Column(String)
    
engine = create_engine(DATABASE_URL, connect_args ={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()