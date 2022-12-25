from input_print_mocking import set_keyboard_input
from unittest import TestCase
from unittest import mock
from unittest.mock import Mock, patch
from vac import Salary
from vac import Vacancy
from vac import InputConnect
from vac import DataSet
import doctest
import vac

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(vac))
    return tests

class SalaryTests(TestCase):
  def test_salary_type(self):
      self.assertEqual(type(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':'True'})).__name__,'Salary')

  def test__salary_salary_from(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':'True'}).salary_from,1)

  def test__salary_salary_to(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':'True'}).salary_to,8)

  def test__salary_salary_currency(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':'True'}).salary_currency,'RUR')
      
  def test__salary_avg(self):
      self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':'True'}).avg(),4.5)

  def test__salary_avg_zero(self):
      self.assertEqual(Salary({'salary_from':0,'salary_to':0,'salary_currency':'RUR','salary_gross':'True'}).avg(),0)

  def test__salary_one_cur_rub(self):
    self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'RUR','salary_gross':'True'}).one_cur(),4.5)

  def test__salary_one_cur_eur(self):
    self.assertEqual(Salary({'salary_from':1,'salary_to':8,'salary_currency':'EUR','salary_gross':'True'}).one_cur(),269.55)

  def test__salary_one_cur_zero(self):
    self.assertEqual(Salary({'salary_from':0,'salary_to':0,'salary_currency':'EUR','salary_gross':'True'}).one_cur(),0)

  def test__salary_on_print(self):
    self.assertEqual(Salary({'salary_from':100,'salary_to':100000,'salary_currency':'EUR','salary_gross':'True'}).on_print(),'100 - 100 000 (Евро) (Без вычета налогов)')

class VacancyTests(TestCase):
  def test_vacancy_type(self):
    self.assertEqual(type(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'})).__name__,"Vacancy")
  
  def test_vacancy_date_year(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'}).published_at.year,2007)

  def test_vacancy_date_month(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'1945-12-03T19:15:55+0300'}).published_at.month,12)
    
  def test_vacancy_date_day(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-20T19:15:55+0300'}).published_at.day,20)

  def test_vacancy_area_name(self):
    self.assertEqual(Vacancy({'name':'asdfa','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'}).area_name,'Test1')

  def test_vacancy_no_name(self):
    self.assertEqual(Vacancy({'name':'','salary_from':'1','salary_to':'8','salary_currency':'RUR','area_name':'Test1','published_at':'2007-12-03T19:15:55+0300'}).name,'')
    
  
  
class InputConnectTests(TestCase):
  def test_input_name(self):
    set_keyboard_input(['test_1.csv','','','','',''])
    self.assertEqual(InputConnect().name,'test_1.csv')

  def test_fr_empty(self):
    set_keyboard_input(['test_1.csv','','','','',''])
    self.assertEqual(InputConnect().fr,'')
  
  def test_fr(self):
    set_keyboard_input(['test_2.csv','','','','3',''])
    self.assertEqual(InputConnect().fr,'3')

  def test_to(self):
    set_keyboard_input(['test_2.csv','','','','3 7',''])
    self.assertEqual(InputConnect().to,'7')

  def test_to(self):
    set_keyboard_input(['test_2.csv','','','','3',''])
    self.assertEqual(InputConnect().to,'')


class DataSetTests(TestCase):
  def test_name(self):
    set_keyboard_input(['test_2.csv','','','','',''])
    self.assertEqual(DataSet(InputConnect()).file_name,'test_2.csv')


