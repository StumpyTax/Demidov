from vac import get_vacs
from stata import get_stat


what_to_print = input("Введите данные для печати(Вакансии\Статистика): ")
if (what_to_print == 'Вакансии'):
    get_vacs()
elif(what_to_print=="Статистика"):
    get_stat()
else:
    print('Неправильный')