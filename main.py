import vac 
import stata 


what_to_print = input("Введите данные для печати(Вакансии\Статистика): ")
if (what_to_print == 'Вакансии'):
    vac.get_vacs()
elif(what_to_print=="Статистика"):
    stata.get_stat()
else:
    print('Неправильный ввод')
