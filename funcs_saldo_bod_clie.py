import pandas as pd
import numpy as np
import plotly.express as px
import datetime

def facts_cleaner(file_name):
  '''
  Clean the dataframe.
  Receives:
    file_name = The txt file exported from contpaqi.
  Returns: the cleaned df.
  '''
  temp = pd.read_table(file_name, encoding = 'latin_1',header = 2,
                         names = ['fecha','folio','razonsocial','total','pendiente','unidades',
                                  'cancelado','metodopago','formapago','uuid','remover'])
  for i in temp.columns:
    if 'remover' in i:
      temp.drop(columns = i, inplace = True)
    else:
      try:
        temp[i] = temp[i].str.strip()
        temp[i] = temp[i].apply(lambda x: x.replace(',',''))
      except AttributeError:
        continue

  temp.razonsocial,temp.total,temp.pendiente,temp.unidades,temp.formapago,temp.metodopago =\
    temp.razonsocial.str.lower(),temp.total.map(float),temp.pendiente.map(float),temp.unidades.map(float),\
    temp.formapago.map(str),temp.metodopago.str.lower()
  temp['fecha'] = pd.to_datetime(temp['fecha'],format = '%d/%m/%Y')

  return temp

def saldo(df, cliente):
  '''
  Shows the amount of consumer debt in money and the cuantity of invoices.
  Receives:
    df = cleaned dataframe from txt file.
    cliente = string with the name (or part of it) of the customer.
  Plot: the amount of debt and the cuantity of invoices.
  Return: a dataframe with the bills due.
  '''
  print('--- ROSA EVELIA ORDAZ LÓPEZ ---')
  temp = df.copy()
  temp = temp[(temp.razonsocial.str.contains(cliente)) & (temp.cancelado == 0) & (temp.pendiente > 0)]
  print('> Estado de cuenta hasta la fecha :',temp.fecha[:1].to_string(index = False))
  print('> Total pendiente :',round(temp.pendiente.sum(),3))
  imag = temp
  imag.set_index('fecha', inplace = True)
  imag.loc[:,'facturas'] = 1
  imag = imag.groupby(imag.index.to_period('M')).sum()
  fig = px.bar(imag, x = imag.index.to_timestamp(), y = 'pendiente', text = 'pendiente',
      title = f'Saldo pendiente por mes y año: {cliente}', height = 300, width = 800)
  fig.show()
  fig = px.bar(imag, x = imag.index.to_timestamp(), y = 'facturas', text = 'facturas',
      title = f'Cantidad de facturas pendientes por mes y año: {cliente}', height = 250, width = 800)
  fig.show()
  return temp.sort_values('fecha', ascending = False)

def facts_grouper(df, fecha_inicio='2016', adeudo=100, days=0, metodo_pago='ppd'):
  '''
  Group the cleaned dataframe from the txt file.
  Receives:
    df = Dataframe cleaned from txt file.
    fecha_inicio = Start date, default 2016.
    adeudo = Min amount owed, default 100.
    days = Min of days elapsed.
    metodo_pago = ppd or pue, default ppd.
  Return: The df grouped with the parameters passed.
  '''
  temp = df.copy()
  temp = temp[(temp.fecha > fecha_inicio) & (temp.pendiente > adeudo) & (temp.cancelado == 0)
              & (temp.metodopago == metodo_pago)]
  if days > 0:
    temp = temp[(temp.fecha < (datetime.datetime.utcnow() - datetime.timedelta(days=days)))]
  temp = temp.groupby('razonsocial').agg(pendiente = ('pendiente','sum'),
                               min_fecha = ('fecha','min'),
                               max_fecha = ('fecha','max'),
                               facturas = ('razonsocial',pd.value_counts)
                              ).sort_values('pendiente', ascending = False).reset_index()
  return temp

def plot_facts(df):
  '''
  Plot the content of the grouped df from cleaned df.
  Receives: Grouped df.
  Plot: Grouped df.
  '''
  fig = px.bar(df, x = 'razonsocial',y = 'pendiente', text = 'pendiente',
      title = 'Saldo pendiente por cliente', height = 700, width = 800)
  fig.update_layout(xaxis = {
    'tickmode': 'array',
    'tickvals': list(range(50)),
    'ticktext': df['razonsocial'].str.slice(start = 0, stop = 25).tolist(),
  })
  fig.show()
  fig = px.bar(df, x = 'razonsocial', y = 'facturas', text = 'facturas',
      title = 'Cantidad de facturas pendientes por cliente', height = 600, width = 800)
  fig.update_layout(xaxis = {
    'tickmode': 'array',
    'tickvals': list(range(50)),
    'ticktext': df['razonsocial'].str.slice(start = 0, stop = 25).tolist(),
  })
  fig.show()
  return df
