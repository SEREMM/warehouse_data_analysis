import pandas as pd
import numpy as np

def cleaner_mov_bod(df, fecha_inicio='2015-01-01', fecha_fin=str(pd.Timestamp.now().date()) ,tipo=0):
  '''
  First clean of the movimientos diarios bod.
    Receives:
      df
      fecha_inicio='2015-01-01'
      fecha_fin=Actual date
      tipo=("gas or ing")
    Returns:
      df: Formated date, date range option, type option.
  '''
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


def cleaner_ped_desc(df, fecha_inicio='2015-01-01', fecha_fin=str(pd.Timestamp.now().date()) ,tipo=0):
  '''
  First clean of the pedidos diarios y descarga diaria.
    Receives:
      df
      fecha_inicio='2015-01-01'
      fecha_fin=Actual date
      tipo=("pedido or descarga")
    Returns:
      df: Formated date, generalized similar concept values, name of clients, date range option, type option.
  '''
  df1 = df
  # date format
  df1['date'] = pd.to_datetime(df1.date, dayfirst=True)
  df1 = df1.sort_values('date')

  # changing values
  # concept
  df1.query('type == "pedido"').loc[df1['concept-camion'].isna(), 'concept-camion'] = 'vde'
  df1['concept-camion'] = df1['concept-camion'].str.lower().str.strip()
  df1.loc[df1['type'] == "pedido", 'concept-camion'] = df1.loc[df1['type'] == "pedido", 'concept-camion'].replace({'moral':'mdo',
                                          'morada':'mdo','grandes':'gde','grande':'gde',
                                          'morados':'mdo','caj':'caja','mdos':'mdo',
                                          'cajas':'caja','reposición':'repo','reposicion':'repo',
                                          'blanco':'bco','muestra':'sin costo','limpio':'bco',
                                          np.nan:'vde','morado':'mdo','verde':'vde'})
  
  # clients
  df1['client-prov'].replace({'miga':'miguel gaytan','raan':'ray andrade','lope':'los pelones',
        'rava':'rafa vallarta','jove':'jose velazquez','cagu':'carlos gutierrez',
        'argu':'armando guzman','casa':'carlos sanchez','ralla':'ramon llanos',
        'leo':'leo cotorro','grusi':'grupo sima','raco':'ramon cortes',
        'ate':'atenas','mafra':'martin franco', 'kaflo':'karina flores',
        'miro':'mizael rodriguez', 'save':'salvador venegas','bomo':'bodeguita movil',
        'as':'as mama', 'rasa':'raul sanchez', 'eltri':'el triunfo', 'pill':'pilly',
        'laz':'lazaro', 'laes':'la escondida', 'ram':'antonio ramirez', 'mex':'el mexicano',
        'hil':'hilario', 'pel':'los pelones', 'and':'and', 'roed':'rosalba edith',
        'gum':'guma', 'elme':'el mexicano', 'rajch':'ramona jch', 'lospe':'los pelones',
        'jealbe':'jesus alberto beltran', 'bar':'barba', 'asma':'as mama', 'jume':'juan meraz',
        'frusa':'fruteria sanli', 'dacha':'daniel chavez', 'gono':'gonio', 'tri':'el triunfo',
        'sava':'salvador vazquez','alal':'aldo almanzar', 'roedce':'rosalba edith', 'gon':'gonio',
        'ramjch':'ramona jch', 'ali':'aliser', 'pil':'pilly', 'ser':'serrano', 'bla':'bla',
        'ragu':'raul guzman','anra':'antonio ramirez', 'bec':'becerro', 'pava':'pablo vazquez',
        'goño':'gonio','venegas':'slavador venegas','mexicano':'el mexicano','triunfo':'el triunfo',
        'delcam':'del campo','ramirez':'antonio ramirez','palo':'pablo lopez','roce':'rosalba edith',
        'bara':'bara', 'miri':'miriam','hila':'hilario','solo':'solorio','ramona':'ramona jch',
        'elmex':'el mexicano','rami':'antonio ramirez', 'bece':'becerro', 'laza':'lazaro',
        'bugarinhijo':'bugarin hijo', 'sima':'grupo sima', 'loor':'lorenzo ordaz', 'bug':'bugarin',
        'isisalc':'isidro slacedo', 'arturo':'arturo arps 20','frufime':'frutas finas meza',
        'frumoflo':'fru montero floresta', 'frumopal':'fru montero palmar', 'suarez':'suarez',
        'fel':'felipe', 'dio':'dionisio','frumonpal':'fru montero palmar','fmonpal':'fru montero palmar',
        'fmonflo':'fru mon floresta','edg':'edgar','delca':'del campo', 'fmon':'fruteria montero',
        'zac':'zacatrapo', 'lualbe':'luis alberto beltran', 'sim':'grupo sima', 'var':'varela',
        'jebe':'jesu alberto beltran','bochi':'boca de chila','frumonflo':'fru montero floresta',
        'leocot':'leo cotorra', 'jorcot':'jorge cotorra','vaivpe':'vanessa ivon', 'punag':'productora ag punta de agua',
        'papa':'productora ag punta de agua', 'guz':'guzman', 'issal':'isidro slacedo','issa':'isidro salcedo',
        'alca':'alianza cabos','alva':'alianza vallarta','alma':'alianza mazatlan','luto':'luis torres',
        'lube':'luis bedolla','mas':'distribuidora masterlim','dima':'distribuidora masterlim',
        'lual':'luis alberto corona mendoza','java':'javier valdez','coav':'comercializadora avelino',
        'vir':'virgilio','alhe':'alfonso hernandez','core':'consuelo reyes','ser':'sergio','bla':'blanca',
        'buga':'bugarin','fel':'felipe','laes':'la escondida','med':'medico','raysa':'ray sanchez',
        'frasa':'francisco snachez','jegui':'jesus guillermo','qui':'quintero',
        'lapema':'la perla mazatleca','eli':'ek','esp':'esparza','poma':'polo martinez',
        'prov':'providencia','gruoz':'grupo ozuna','jucru':'juan cruz','ansa':'antonio sanchez',
        'jorav':'jorge cotorra','fera':'felix ramirez','bra':'brafermaz','brafe':'brafermaz',
        'cadu':'carlos duran','kar':'alex karla','bara':'barajas','suamsu':'super amigos super',
        'suamar':'super amigos arcos','dame':'daniel mercedez','gua':'guayabitos',
        'zir':'ziracua','arfro':'arbol frondoso','damer':'daniel mercedes','jepa':'jesus paez',
        'ares':'armida esmeralda iglesias','mir':'miriam'},
        inplace=True)

  # date range
  df1 = df1[(df1.date >= fecha_inicio) & (df1.date < fecha_fin)]

  # selecting type
  if tipo == 'pedido':
    df1 = df1.query('type == "pedido"')
  elif tipo == 'descarga':
    df1 = df1.query('type == "descarga"')

  return df1
