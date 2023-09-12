from django.test import TestCase
from scheduling_app.sis_api import Semester, By, CourseQuery

"""
If you get: 
    django.core.exceptions.ImproperlyConfigured: 
        Requested setting LOGGING_CONFIG, but settings are not configured. 
        You must either define the environment variable DJANGO_SETTINGS_MODULE 
        or call settings.configure() before accessing settings.
Then in your IDE specify the environment variable: "DJANGO_SETTINGS_MODULE=schedule_advisor.settings" for each test
"""
class SISApi(TestCase):
    def test_find_by_instructor(self):
        data = CourseQuery.find(By.instructor('McBurney')).text
        self.assertTrue(data.__contains__('McBurney'))

    def test_find_by_subject(self):
        data = CourseQuery.find(By.subject('CS')).text
        self.assertTrue(data.__contains__('CS'))

    def test_find_by_term_2023_spring(self):
        data = CourseQuery.find(By.term(2023, Semester.SPRING)).text
        self.assertTrue(data.__contains__('1232'))

    def test_find_by_term_2020_fall(self):
        data = CourseQuery.find(By.term(2020, Semester.FALL)).text
        self.assertTrue(data.__contains__('1208'))

    def test_find_by_term_2008_summer(self):
        data = CourseQuery.find(By.term(2008, Semester.SUMMER)).text
        self.assertTrue(data.__contains__('1086'))

    def test_find_by_catalog_number(self):
        data = CourseQuery.find(By.catalog_number(3140)).text
        self.assertTrue(data.__contains__('3140'))

    def test_find_by_major_identifiers(self):
        data = CourseQuery.find(
            By.subject('CS'),
            By.catalog_number(3140),
            By.term(2022, Semester.FALL),
            By.instructor('McBurney')
        ).text
        self.assertTrue(data.__contains__('CS'))
        self.assertTrue(data.__contains__('3140'))
        self.assertTrue(data.__contains__('Paul McBurney'))
        self.assertTrue(data.__contains__('1228'))

    def test_find_by_page_1(self):
        data = CourseQuery.find(By.subject('CS'), By.page(1), By.term(2021, Semester.SUMMER)).text
        self.assertTrue(data.__contains__('CS'))
        self.assertTrue(data.__contains__('1216'))

    def test_find_by_page_2(self):
        data = CourseQuery.find(By.subject('CS'), By.page(2), By.term(2021, Semester.SUMMER)).text
        self.assertTrue(data.__contains__('CS'))
        self.assertTrue(data.__contains__('1216'))

    def test_find_by_page_3(self):
        data = CourseQuery.find(By.subject('CS'), By.page(3), By.term(2021, Semester.SUMMER)).text
        self.assertTrue(data.__contains__('[]'))