import csv
import os
import requests
import datetime

def get_data():
  res=[]
  for hours in [i*3 for i in range(8)]:
    for j in range(20):
      fromh=hours if hours>=10 else '0'+str(hours)
      toh=hours+2 if hours+2>=10 else '0'+str(hours+2)
      headers={'User-Agent':'MyApp/1.0 (pikachu75311@gmail.com)'}
      response=requests.get(f'https://api.hh.ru/vacancies?specialization=1&date_from=2022-12-22T{fromh}:00:00&date_to=2022-12-22T{toh}:59:00&per_page=100&page={j}')
      resp_json=response.json()
      for vac in resp_json['items']:
        salary=vac['salary']
        if(salary==None):
          salary={}
          salary['to']=''
          salary['from']=''
          salary['currency']=''

        res.append({'name':vac['name']
                  ,'salary_from':salary['from']
                  ,'salary_to':salary['to']
                  ,'salary_currency':salary['currency']
                  ,'area_name':vac['area']['name']
                  ,'published_at':vac['published_at']})
    
  with open(f'.\\data\\data.csv', 'w', newline='' ,encoding="utf-8-sig") as f:
      w = csv.writer(f, delimiter=',',    
      quotechar='|', quoting=csv.QUOTE_MINIMAL)
      w.writerow(['name','salary_from','salary_to','salary_currency','area_name','published_at'])
      for row in res:
        w.writerow(row.values())

if(__name__=='__main__'):
  get_data()