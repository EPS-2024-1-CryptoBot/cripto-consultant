from sqlalchemy import create_engine, Column, String, Float, Integer, Time, Enum, DateTime
from sqlalchemy.sql import func # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
import os

Base = declarative_base()

class StrategyType(enum.Enum):
    TECHNICAL = 'Technical'
    BREAKOUT = 'Breakout'

    def __str__(self) -> str:
        return self.value
    
class TimeFrameType(enum.Enum):
    ONE_MINUTE = '1m'
    FIVE_MINUTES = '5m'
    FIFTEEN_MINUTES = '15m'
    THIRTY_MINUTES = '30m'
    ONE_HOUR = '1h'

class PlatformType(enum.Enum):
    BINANCE = 'Binance'
    BITMEX = 'Bitmex'

    def __str__(self) -> str:
        return self.value

class Trade(Base):
    __tablename__ = 'trades'
    __table_args__ = {"schema": "trades"}

    id = Column(String, primary_key=True, unique=True, nullable=False)
    platform = Column(Enum(PlatformType), nullable=False)
    api_key = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    strategy = Column(Enum(StrategyType), nullable=False)
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

# Create an engine
engine = create_engine(os.environ.get('DB_URL'))
# # Create all tables
Base.metadata.create_all(engine)


# # Create a configured "Session" class
Session = sessionmaker(bind=engine)

# # Create a Session
session = Session()

# # Add a new trade
# new_trade = Trade(
#     time='12:00:00',  # Assuming 'time' is given in HH:MM:SS format
#     exchange='Binance',
#     strategy='Scalping',
#     side='Buy',
#     quantity=1.5,
#     status='Open',
#     pnl='+10%'
# )

# # Add the trade to the session
# session.add(new_trade)

# # Commit the transaction
# session.commit()
