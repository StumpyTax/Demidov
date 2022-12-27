import csv
import os
from os import SEEK_END


def recycle(file_name:str)->None:
  '''
  Считывает csv файл и разбивает на csv файлы по годам

  Args:
      file_name (str): Имя файла
  '''
  res={}
  for file in os.listdir('.\\data'):
    os.remove('.\\data\\'+file)

  with open(ﬁle_name, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
      if(row['published_at'][0:4] in res.keys()):
        res[row['published_at'][0:4]].append(list(row.values()))
      else:
        res[row['published_at'][0:4]]=[list(row.values())]

    if (f.seek(0, SEEK_END)==0):
      print('Пустой файл')
      exit()
    elif (res.__len__()==0):
      print('Нет данных')
      exit()
    
    curr_conv(res)
    

def curr_conv(res):
  '''
  Конвертирует валюты в рубли и сохраняет в csv файлы по годам

  Args:
      res (_type_): Вакансии
  '''
  for year in res.keys():
    fieldnames=['name','salary','area_name','published_at']
    with open(f'.\\data\\{year}.csv', 'w', newline='' ,encoding="utf-8-sig") as f:
      w = csv.writer(f, delimiter=',',    
      quotechar='|', quoting=csv.QUOTE_MINIMAL)
      w.writerow(fieldnames)
      curs_k={}
      with open(f'.\\cur\\{year}.csv', encoding="utf-8-sig") as cur:
          reader = csv.DictReader(cur)
          for r in reader:
            curs_k[r['Date'][5:]]=r

      for row in res[year]:

        if(row[3] not in reader.fieldnames ):
          continue
        k=curs_k[row[5][5:7]][row[3]]
        
        salary=0
        if (row[1]=='' and row[2]=='' or k==''):
          salary=""
        elif (row[2]==''):
          salary=float(row[1])*float(k)
        elif(row[1]==''):
          salary=float(row[2])*float(k)
        else:
          salary=((float(row[1])+float(row[2]))/2)*float(k)
        w.writerow(['"'+row[0]+'"',salary,'"'+row[4]+'"','"'+row[5]+'"'])


if (__name__=='__main__'):
  recycle('vacancies_dif_currencies.csv')