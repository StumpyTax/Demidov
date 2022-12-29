import os
import pandas
import math
import numpy as np

curs_k=pandas.read_csv('.\\cur\\сur.csv')
currs=curs_k.columns.values.tolist()
# def recycle(file_name:str)->None:
#   '''
#   Считывает csv файл и разбивает на csv файлы по годам

#   Args:
#       file_name (str): Имя файла
#   '''
#   for file in os.listdir('.\\data'):
#     os.remove('.\\data\\'+file)




def curr_conv(row):
  '''
  Конвертирует валюты в рубли и сохраняет в csv файлы по годам

  Args:
      res (_type_): Вакансии
  '''
  f=float(row.salary_from)
  to=float(row.salary_to)
  cur=row.salary_currency

  if (math.isnan(f) and math.isnan(to)):
      return None
  if (cur not in currs):
      return None

  k=0
  if (cur != 'RUR'):
    k = curs_k[curs_k["Date"] == row["published_at"][0:7]][cur].values
    try:
        k = float(k)
    except:
        return None
  else:
    k = 1

  salary=None
  if (math.isnan(f) or math.isnan(to)):
    if (math.isnan(f)):
      salary=to*k
    else:
      salary=f*k
  else:
    salary=((f+to)/2)*k
  
  return salary

if (__name__=='__main__'):
# def kk():
  df=pandas.read_csv('vacancies_dif_currencies.csv')
  # df=pandas.read_csv('s.csv')
  data={"name": [], "salary": [], "area_name": [], "published_at": []}
  ndf=pandas.DataFrame(data)
  ndf.name=df.name
  ndf.area_name=df.area_name
  ndf.published_at=df.published_at

  ndf.salary=(df.apply(curr_conv,axis=1))
  ndf.to_csv('.\\data\\data.csv')

  # recycle('vacancies_dif_currencies.csv') 
  # recycle('s.csv')