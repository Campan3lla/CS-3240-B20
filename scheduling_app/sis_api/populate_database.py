import json

from scheduling_app.sis_api import CourseQuery, By, CourseJSONRetrieval


def fill_database_by_query(*args):
    data = ''
    page_index = 0
    course_set = set()
    while data != '[]':
        page_index += 1
        data = CourseQuery.find(*args, By.page(page_index)).text
        course_list_json = json.loads(data)
        current_courses = CourseJSONRetrieval.get_course_set(course_list_json)
        course_set = course_set.union(current_courses)
    return course_set