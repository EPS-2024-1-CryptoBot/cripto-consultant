import datetime
import json
import logging
import tkinter as tk
import typing
from datetime import datetime
from tkinter.messagebox import askquestion

from connectors.binance import BinanceClient
from connectors.bitmex import BitmexClient
from database import WorkspaceData
from interface.autocomplete_widget import Autocomplete
from interface.logging_component import Logging
from interface.scrollable_frame import ScrollableFrame
from interface.strategy_component import StrategyEditor
from interface.styling import (BG_COLOR, BG_COLOR_2, BOLD_FONT, FG_COLOR,
                               FG_COLOR_2, GLOBAL_FONT)
from interface.trades_component import TradesWatch
from interface.watchlist_component import Watchlist
from models import Contract, Trade
from strategies.strategies import BreakoutStrategy, TechnicalStrategy

from consultant.utils import check_float_format, check_integer_format
