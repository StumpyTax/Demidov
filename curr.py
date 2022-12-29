import requests
import csv
import xmltodict
import os
import xml
from xml.etree import ElementTree
from pandas import DataFrame
import datetime
from os import SEEK_END


def get_curs(file_name:str)->None:
  '''
  Получение курсов валют из вакансий, по годам и месяцам.

  Args:
      file_name (str): Имя файла с вакансиями
  '''
  curs_freq={}
  oldest_date=datetime.date(year=9999,day=1,month=1)
  newest_date=datetime.date(year=1900,day=1,month=1)

  with open(ﬁle_name, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        temp=datetime.date(year=int(row['published_at'][0:4]),month=int(row['published_at'][5:7]),day=int(row['published_at'][8:10]))
        if(oldest_date>temp):
          oldest_date=temp
        elif (temp>newest_date):
          newest_date=temp
        if(row['salary_currency']==''):
          continue
        if(row['salary_currency'] in curs_freq.keys()):
          curs_freq[row['salary_currency']]+=1
        else:
          curs_freq[row['salary_currency']]=1
          
  data={'Date':[]}
  for i in curs_freq.items():
    if(i[1]>=5000):
      data[i[0]]=[]

  for year in range(newest_date.year-oldest_date.year+1):
    for i in range(1,13):
      data['Date'].append(f'{oldest_date.year+year}-{i if (i//10==1) else f"0{i}"}')
      m=str(i)
      if(m.__len__()==1):
        m='0'+m
      response=requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=15/{m}/{oldest_date.year+year}')
      xmld=xmltodict.parse(response.content)
      for j in xmld['ValCurs']['Valute']:
        if(j['CharCode'] not in data.keys()):
          continue
        data[j['CharCode']].append(float(j['Value'].replace(',','.'))/float(j['Nominal']))
      data['RUR'].append(1)
      for j in data.keys():
        if(data[j].__len__()<data['Date'].__len__()):
          data[j].append('')
  d=DataFrame(data)
  d.index.rename('№',inplace=True)
  d.to_csv(f'.\\cur\\сur.csv',encoding="utf-8-sig")


if (__name__=='__main__'):
  get_curs('vacancies_dif_currencies.csv')