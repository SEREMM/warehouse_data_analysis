import pandas as pd
import numpy as np

def pre1_mov_bod(df, fecha_inicio='2015-01-01', fecha_fin=str(pd.Timestamp.now().date()) ,tipo=0, ):
  df1 = df.copy()
  # date format
  lista = []
  for i in df1.date:
    if '/' in i:
      temp = i.split('/')
      temp = temp[2] + '-' + temp[1] + '-' + temp[0]
      lista.append(temp)
    else:
      lista.append(i)

  df1['date'] = pd.to_datetime(lista)
  df1 = df1.sort_values('date')

  # date range
  df1 = df1[(df1.date >= fecha_inicio) & (df1.date < fecha_fin)]

  # gas or ing
  if tipo == 'gas':
    df1 = df1.query('type == "gas"')
  elif tipo == 'ing':
    df1 = df1.query('type == "ing"')

  return df1
