from input_print_mocking import set_keyboard_input
from unittest import TestCase
from unittest import mock
from unittest.mock import Mock, patch
from stata import Salary
from stata import Vacancy
from stata import InputConnect
from stata import DataSet
from stata import Report
import doctest
import stata

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(stata))
    return tests


class SalaryTests(TestCase):
  def test_salary_type(self):
      self.assertEqual(type(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':True})).__name__,'Salary')

  def test__salary_salary_from(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':True}).salary_from,1)

  def test__salary_salary_to(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':True}).salary_to,8)

  def test__salary_salary_currency(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':True}).salary_currency,'RUR')
      
  def test__salary_avg(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':True}).avg(),4.5)

  def test__salary_avg_zero(self):
      self.assertEqual(Salary({'salary_from':0,'salary_to':0,'salary_currency':'RUR','salary_gross':True}).avg(),0)

  def test__salary_one_cur_rub(self):
    self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':True}).one_cur(),4.5)

  def test__salary_one_cur_eur(self):
    self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'EUR','salary_gross':True}).one_cur(),269.55)

  def test__salary_one_cur_zero(self):
    self.assertEqual(Salary({'salary_from':0,'salary_to':0,'salary_currency':'EUR','salary_gross':True}).one_cur(),0)

class VacancyTests(TestCase):
  def test_vacancy_type(self):
    self.assertEqual(type(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'})).__name__,"Vacancy")
  
  def test_vacancy_date_year(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'}).date.year,2007)

  def test_vacancy_date_month(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'1945-12-03T19:15:55+0300'}).date.month,12)
    
  def test_vacancy_date_day(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-20T19:15:55+0300'}).date.day,20)

  def test_vacancy_area_name(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'}).area_name,'Test1')

  def test_vacancy_no_name(self):
    self.assertEqual(Vacancy({'name':'','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'}).name,'')
  
class InputConnectTests(TestCase):
  def test_input_name(self):
    set_keyboard_input(['test_1.csv',''])
    self.assertEqual(InputConnect().name,'test_1.csv')

  def test_data(self):
    set_keyboard_input(['test_1.csv','Программист'])
    self.assertEqual(InputConnect().vacancies_data.salary_dynamic[2007],7500)

class DataSetTests(TestCase):
  def test_name(self):
    set_keyboard_input(['test_2.csv',''])
    self.assertEqual(DataSet(InputConnect()).file_name,'test_2.csv')

  def test_top_10(self):
    set_keyboard_input(['test_2.csv',''])
    data_set=DataSet(InputConnect())
    self.assertEqual(data_set.get_top_10(data_set.salary_dynamic)[2007],44295)

  def test_amount_dynamic(self):
    set_keyboard_input(['test_2.csv',''])
    data_set=DataSet(InputConnect())
    self.assertEqual(data_set.amount_dynamic[2007],11)

  def test_amount_dynamic_city(self):
    set_keyboard_input(['test_2.csv',''])
    data_set=DataSet(InputConnect())
    self.assertEqual(data_set.amount_dynamic_city['Екатеринбург'],0.0909)
  
  def test_amount_dynamic_city(self):
    set_keyboard_input(['test_2.csv','Программист'])
    data_set=DataSet(InputConnect())
    self.assertEqual(data_set.amount_dynamic_prof[2007],3)

  def test_salary_dynamic_city(self):
    set_keyboard_input(['test_2.csv','Программист'])
    data_set=DataSet(InputConnect())
    self.assertEqual(data_set.salary_dynamic_city['Екатеринбург'],22500)

  def test_salary_dynamic_city(self):
    set_keyboard_input(['test_2.csv','Программист'])
    data_set=DataSet(InputConnect())
    self.assertEqual(data_set.salary_dynamic_prof[2007],29166)

