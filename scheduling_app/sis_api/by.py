import re
from enum import Enum



class Semester(Enum):
    FALL = 8
    SPRING = 2
    SUMMER = 6


class By:
    @staticmethod
    def subject(name):
        return f'&subject={name}'

    @staticmethod
    def instructor(instructor):
        name_pieces = re.findall('[a-zA-Z]+', instructor)
        query: str = ''
        for name_part in name_pieces:
            query += f'&instructor_name={name_part}'
            print(name_part)
        return query

    @staticmethod
    def term(year: int, semester: Semester):
        return f'&term=1{(year % 100):02}{semester.value}'

    @staticmethod
    def catalog_number(catalog_number: int):
        return f'&catalog_nbr={catalog_number}'

    @staticmethod
    def page(page_number: int):
        return f'&page={page_number}'

    @staticmethod
    def class_number(class_number: int):
        return f'&class_nbr={class_number}'

    @staticmethod
    def keyword(keyword: str):
        return f'&keyword={keyword}'
