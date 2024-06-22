from sqlalchemy import create_engine, Column, String, Float, Enum, DateTime
from sqlalchemy.sql import func # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import enum
import os

Base = declarative_base()
schema = os.environ.get('DB_SCHEMA')

class StrategyType(enum.Enum):
    TECHNICAL = 'Technical'
    BREAKOUT = 'Breakout'
    
class TimeFrameType(enum.Enum):
    ONE_MINUTE = '1m'
    FIVE_MINUTES = '5m'
    FIFTEEN_MINUTES = '15m'
    THIRTY_MINUTES = '30m'
    ONE_HOUR = '1h'

class PlatformType(enum.Enum):
    BINANCE = 'Binance'
    BITMEX = 'Bitmex'

class Trade(Base):
    __tablename__ = 'trades'
    __table_args__ = {"schema": schema}

    id = Column(String, primary_key=True, unique=True, nullable=False)
    platform = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    strategy = Column(String, nullable=False)
    coin = Column(String, nullable=False)
    timeframe = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    rsi_period = Column(Float, nullable=True)
    macd_fast = Column(Float, nullable=True)
    macd_slow = Column(Float, nullable=True)
    macd_signal = Column(Float, nullable=True)
    minimum_volume = Column(Float, nullable=True)
    last_execution = Column(DateTime(timezone=True), server_default=func.now())

engine = create_engine(os.environ.get('DB_URL'))

schema_creation = text(f"CREATE SCHEMA IF NOT EXISTS {schema};")
with engine.connect() as conn:
    conn.execute(schema_creation)
    conn.commit()

Base.metadata.schema = schema
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()