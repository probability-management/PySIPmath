#!/usr/bin/env python

from PySIP import Json
from pandas import read_csv

Json(
    read_csv("./example/Dev_Time_Lib.csv"), 
    "Dev_Time_Lib.SIPmath",
    "Example User"
)
