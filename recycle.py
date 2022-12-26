import csv
import os
from os import SEEK_END


def recycle(file_name:str)->None:
  res={}
  for file in os.listdir('.\\data'):
    os.remove('.\\data\\'+file)

  with open(ﬁle_name, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
      if (all(row.values()) and row.values().__len__() == reader.fieldnames.__len__()):
        if(row['published_at'][0:4] in res.keys()):
          res[row['published_at'][0:4]].append(row.values())
        else:
          res[row['published_at'][0:4]]=[row.values()]

    if (f.seek(0, SEEK_END)==0):
      print('Пустой файл')
      exit()
    elif (res.__len__()==0):
      print('Нет данных')
      exit()

  for year in res.keys():
    with open(f'.\\data\\{year}.csv', 'w', newline='' ,encoding="utf-8-sig") as f:
      w = csv.writer(f, delimiter=',',    
      quotechar='|', quoting=csv.QUOTE_MINIMAL)
      w.writerow(reader.fieldnames)
      w.writerows(res[year])


if (__name__=='__main__'):
  recycle('v.csv')