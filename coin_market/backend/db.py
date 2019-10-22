''' Collection of tools for interacting with the DB '''
from sqlalchemy import Column, String, Integer, Float, Date, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DailyPriceListing(Base):
    __tablename__ = 'daily_price_listings'
    
    asset_id = Column(String, primary_key=True)
    effective_date = Column(Date, primary_key=True)
    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)
    volume_traded = Column(Float)
    trades_count = Column(Integer)
    updated_at = Column(DateTime)

class DBService:
    ''' Abtraction for working with basic db tasks '''
    def __init__(self, sql_url):
        self.engine = create_engine(sql_url)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def connect(self):
        return self.engine.connect()

