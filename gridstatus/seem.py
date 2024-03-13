import copy
import io
import time
import warnings
from contextlib import redirect_stderr
from zipfile import ZipFile

import pandas as pd
import requests
import tabula
from tabulate import tabulate
from termcolor import colored

from gridstatus import utils
from gridstatus.base import (
    GridStatus,
    ISOBase,
    Markets,
    NoDataFoundException,
    NotSupported,
)




class SEEM(ISOBase):
    """
    South Eastern Energy Market (SEEM) class

    https://southeastenergymarket.com/reports-form/
    """
    def __init__(self):
        super().__init__()
        self.name = "SEEM"
        self.market = Markets.SOUTHEASTERN
        self.timezone = "US/Eastern"
        self._data = None
