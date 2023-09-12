import requests


class CourseQuery:
    URL = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula' \
          '.IScript_ClassSearch?institution=UVA01'

    @staticmethod
    def find(*args):
        url_string = CourseQuery.URL
        for restriction in args:
            url_string += restriction
        return requests.get(url_string)
