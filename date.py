import os
from datetime import date,datetime


def dateTime():
  """Retorna data e hora atual"""
  return str(datetime.today().strftime("%m/%d/%Y  %H:%M:%S"))


print(dateTime())