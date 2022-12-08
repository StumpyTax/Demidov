import csv, re, prettytable, datetime
from os import SEEK_END
from prettytable import PrettyTable
from typing import List, Dict, Tuple, Any


class InputConnect:
    def __init__(self):
        self.name = input('Введите название файла: ').strip()
        self.filter = input('Введите параметр фильтрации: ').strip()
        self.sort_field = input('Введите параметр сортировки: ').strip()
        self.revers = input('Обратный порядок сортировки (Да / Нет): ').strip()
        self.__numb = input('Введите диапазон вывода: ').strip()
        self.fields = input('Введите требуемые столбцы: ').split(', ')
        self.fr = ''
        self.to = ''
        if (self.revers == ''):
            self.revers = "Нет"
        if (self.__numb != '' and self.__numb.count(' ') > 0):
            self.__numb = self.__numb.split(' ')
        if (self.__numb.__len__() == 2):
            self.fr, self.to = self.__numb
        else:
            self.fr = self.__numb
        self.__validation()
        self.vacancies_data = DataSet(self)

    def __validation(self) -> None:
        fields_names = ['Навыки',
                        'Оклад',
                        'Дата публикации вакансии',
                        'Опыт работы',
                        'Премиум-вакансия',
                        'Идентификатор валюты оклада',
                        'Название',
                        'Название региона',
                        'Компания']

        if (not self.sort_field in fields_names and self.sort_field != ''):
            print('Параметр сортировки некорректен')
            exit()
        if (self.revers != "Да" and self.revers != "Нет"):
            print('Порядок сортировки задан некорректно')
            exit()
        if (not self.filter.__contains__(':') and self.filter != ""):
            print('Формат ввода некорректен')
            exit()
        if (not fields_names.__contains__(self.filter.split(': ')[0]) and self.filter != ""):
            print('Параметр поиска некорректен')
            exit()

    def print_vacancies(self) -> None:

        dic_naming = {"name": "Название",
                      "description": "Описание",
                      "key_skills": "Навыки",
                      "experience_id": "Опыт работы",
                      "premium": "Премиум-вакансия",
                      "employer_name": "Компания",
                      "salary": "Оклад",
                      "area_name": "Название региона",
                      "published_at": "Дата публикации вакансии"}
        salary_added=True
        if (self.fields[0] == ''):
            self.fields[0]="№"
            for i in self.vacancies_data.fieldnames:
                if("salary" in i ):
                    if(salary_added):
                        self.fields.append(dic_naming['salary'])
                        salary_added=False
                else: self.fields.append(dic_naming[i])
        else:
            self.fields.insert(0, '№')

        table = PrettyTable(encodings='utf-8-sig', field_names=list(dic_naming.values()))
        table.add_autoindex('№')
        table.max_width = 20
        table.align = "l"
        table.hrules = prettytable.ALL

        if (self.fr == ""):
            self.fr = 1
        if (self.to == ""):
            self.to = self.vacancies_data.vacancies_objects.__len__() + 1

        self.fr, self.to = int(self.fr), int(self.to)

        for i, vac in enumerate(self.vacancies_data.vacancies_objects, 1):
            table.add_row([i] + list(vac.values()))
        print(table.get_string(start=self.fr - 1 if self.fr != 0 else self.fr, end=self.to - 1, fields=self.fields))


class Vacancy:
    def __init__(self, v: dict) -> None:
        vac = self.__clear(v)
        self.name = ''
        self.description = ""
        self.key_skills = ''
        self.experience_id = ''
        self.premium = ''
        self.employer_name = ''
        self.salary = ''
        self.area_name = ''
        self.published_at = ''

        initi={"name": lambda vac:self.__set_name(vac),
               "description": lambda vac:self.__set_descr(vac),
               "key_skills": lambda vac:self.__set_key_skills(vac),
               "experience_id": lambda vac:self.__set_experience_id(vac),
               "premium": lambda vac:self.__set_premium(vac),
               "employer_name": lambda vac:self.__set_employer_name(vac),
               "salary": lambda vac:self.__set_salary(vac),
               "area_name": lambda vac:self.__set_area_name(vac),
               "published_at": lambda vac:self.__set_published_at(vac)}

        salary_seted=True

        for i in v.keys():
            if('salary' in i):
                if(salary_seted):
                    initi['salary'](vac)
                    salary_seted=False
            else:
                initi[i](vac)

    def __set_name(self,vac):
        self.name=vac['name']

    def __set_descr(self,vac):
        self.description = vac['description']

    def __set_key_skills(self,vac):
        self.key_skills = vac['key_skills'].split('\n')

    def __set_experience_id(self,vac):
        self.experience_id = vac['experience_id']

    def __set_premium(self,vac):
        self.premium = vac['premium']

    def __set_employer_name(self,vac):
        self.employer_name=vac["employer_name"]

    def __set_salary(self,vac):
        self.salary = Salary(vac=vac)

    def __set_area_name(self,vac):
        self.area_name = vac['area_name']

    def __set_published_at(self,vac):
        self.published_at = datetime.datetime.strptime(vac['published_at'], "%Y-%m-%dT%H:%M:%S%z")


    def __clear(self, vac: dict) -> dict:
        n_dict = {}
        for item in vac.items():
            l = item[1]
            l = re.sub(r"<[^>]+>", "", l, flags=re.S)
            l = re.sub(r" +", ' ', l)
            l = re.sub(r"\u2002", "", l)
            l = re.sub(r"\xa0", " ", l)
            l = l.strip()
            n_dict[item[0]] = l
        return n_dict

    def formatter(self) -> None:
        res = {}
        true_false = {"True": "Да", "False": "Нет"}
        form = {"experience_id": lambda item: (exp[item]),
                "published_at": lambda item: (item.strftime('%d.%m.%Y')),
                "premium": lambda item: (true_false[item]),
                "name": lambda item: (item),
                "description": lambda item: (item),
                "key_skills": lambda item: ((self.__skils_to_str())),
                "employer_name": lambda item: (item),
                "area_name": lambda item: (item),
                "salary": lambda item: (item.on_print())
                }

        for item in self.__dict__.items():
            if(item[1]==""):
                continue
            on_print = form[item[0]](item[1])
            if (on_print.__len__() > 100):
                on_print = on_print[0:100] + "..."
            self.__setattr__(item[0], on_print)

    def __skils_to_str(self):
        skills = ''
        for skill in self.key_skills:
            skills += skill + '\n'
        return skills.strip()

    def values(self) -> list:
        return [self.name, self.description, self.key_skills, self.experience_id, self.premium, self.employer_name,
                self.salary, self.area_name, self.published_at]


class DataSet:

    def csv_parsing(func):
        def parsing(self, data: InputConnect):
            vac, head = func(data.name)

            if (data.sort_field != ""):
                exp_for_sort = dict(zip(exp.keys(), [0, 1, 2, 3]))

                sort_dic = {
                    'Навыки': lambda vac: vac.key_skills.__len__(),
                    'Оклад': lambda vac: vac.salary.one_cur(),
                    'Дата публикации вакансии': lambda vac: vac.published_at,
                    'Опыт работы': lambda vac: exp_for_sort[vac.experience_id],
                    'Премиум-вакансия': lambda vac: bool(vac.premium),
                    'Название': lambda vac: vac.name,
                    'Название региона': lambda vac: vac.area_name,
                    'Компания': lambda vac: vac.employer_name
                }
                reverse = {"Да": True, "Нет": False}[data.revers]
                vac.sort(key=sort_dic[data.sort_field], reverse=reverse)

            return self.csv_filter(vacations=vac, data=data),head

        return parsing

    def csv_ﬁlter(self, vacations: list, data: InputConnect):
        newBody = list()
        for vac in vacations:
            if (self.filtration(data.filter, vac)):
                vac.formatter()
                newBody.append(vac)

        if (newBody.__len__() == 0):
            print('Ничего не найдено')
            exit()
        return newBody

    def filtration(self, filter: str, vac: Vacancy) -> bool:
        if (filter == ""):
            return True

        field = filter.split(': ')
        value = field[1]
        field = field[0]
        filter_dic = {
            'Навыки': lambda value: ((set(str(value).split(', '))).issubset(set(vac.key_skills))),
            'Оклад': lambda value: (
                        float(vac.salary.salary_from) <= float(value) and float(vac.salary.salary_to) >= float(value)),
            'Дата публикации вакансии': lambda value: (vac.published_at.strftime('%d.%m.%Y') == value),
            'Опыт работы': lambda value: (exp[vac.experience_id] == value),
            'Премиум-вакансия': lambda value: ({"True": "Да", "False": "Нет"}[vac.premium] == value),
            'Идентификатор валюты оклада': lambda value: (cur[vac.salary.salary_currency] == value),
            'Название': lambda value: (vac.name == value),
            'Название региона': lambda value: (vac.area_name == value),
            'Компания': lambda value: (vac.employer_name == value)
        }
        return filter_dic[field](value)

    @csv_parsing
    def сsv_reader(ﬁle_name: str) -> list:
        with open(ﬁle_name, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            res = []
            for row in reader:
                if (all(row.values()) and row.values().__len__() == reader.fieldnames.__len__()):
                    vac = Vacancy(row)
                    res.append(vac)

            if (f.seek(0, SEEK_END) == 0):
                print('Пустой файл')
                exit()
            elif (res.__len__() == 0):
                print('Нет данных')
                exit()
            return res, reader.fieldnames

    def __init__(self, data: InputConnect) -> None:
        self.file_name = data.name
        self.vacancies_objects, self.fieldnames = self.сsv_reader(data)


class Salary:

    def __init__(self, vac: dict) -> None:
        self.salary_from =''
        self.salary_to = ''
        self.salary_gross = ''
        self.salary_currency=''

        initi={'salary_from': lambda vac: self.__set_salary_from(vac),
        'salary_to':lambda vac: self.__set_salary_to(vac),
        'salary_gross':lambda vac: self.__set_salary_gross(vac),
        'salary_currency':lambda vac: self.__set_salary_currency(vac)}

        for i in vac.keys():
            if('salary' in i):
                initi[i](vac)

    def __set_salary_from(self,vac):
        self.salary_from = vac['salary_from']

    def __set_salary_to(self,vac):
        self.salary_to = vac['salary_to']

    def __set_salary_gross(self,vac):
        self.salary_gross = vac['salary_gross']

    def __set_salary_currency(self,vac):
        self.salary_currency = vac['salary_currency']

    def avg(self) -> float:
        return (float(self.salary_from) + float(self.salary_to)) / 2

    def on_print(self) -> str:
        return "{0:,} - {1:,} ({2}) ({3})".format(int(float(self.salary_from)),
                                                  int(float(self.salary_to)),
                                                  cur[self.salary_currency],
                                                  taxes[self.salary_gross]).replace(',', ' ')

    def one_cur(self):
        currency_to_rub = {
            "AZN": 35.68,
            "BYR": 23.91,
            "EUR": 59.90,
            "GEL": 21.74,
            "KGS": 0.76,
            "KZT": 0.13,
            "RUR": 1,
            "UAH": 1.64,
            "USD": 60.66,
            "UZS": 0.0055,
        }
        return self.avg() * currency_to_rub[self.salary_currency]


cur = {"AZN": "Манаты",
       "BYR": "Белорусские рубли",
       "EUR": "Евро",
       "GEL": "Грузинский лари",
       "KGS": "Киргизский сом",
       "KZT": "Тенге",
       "RUR": "Рубли",
       "UAH": "Гривны",
       "USD": "Доллары",
       "UZS": "Узбекский сум"}

exp = {"noExperience": "Нет опыта",
       "between1And3": "От 1 года до 3 лет",
       "between3And6": "От 3 до 6 лет",
       "moreThan6": "Более 6 лет"}

taxes = {"False": "С вычетом налогов", "True": "Без вычета налогов","":''}

def  get_vacs():
    data = InputConnect()
    data.print_vacancies()
