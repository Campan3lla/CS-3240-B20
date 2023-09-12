import datetime
import json
import os
from django.test import TestCase


from scheduling_app.models import Meeting, Location, CourseIdentifier, Instructor, RegistrationInformation, Course, \
    EnrollmentInformation
from scheduling_app.sis_api import CourseJSONRetrieval

#test_loc = '/home/runner/work/project-b-20/project-b-20/scheduling_app/tests/'
# add to correct pathing
file_dir = os.path.dirname(os.path.realpath('__file__'))
file_name_course = os.path.join(file_dir, 'scheduling_app/tests/resources/course.json')
file_name_list = os.path.join(file_dir, 'scheduling_app/tests/resources/course_list.json')
file_name_no_loc = os.path.join(file_dir, 'scheduling_app/tests/resources/course_meeting_without_location.json')

class TestCourseJSONRetrieval(TestCase):
    meeting_json: json
    course_json: json

    def setUp(self) -> None:
        with open(file_name_course, 'r') as course_file:
            self.course_json = json.loads(course_file.read())
        self.meeting_json = self.course_json['meetings'][0]

    def test_get_date(self):
        json_date = self.meeting_json['start_dt']
        self.assertEqual(datetime.date(2023, 8, 22), CourseJSONRetrieval.get_date(json_date))

    def test_get_time(self):
        json_time = self.meeting_json['start_time']
        self.assertEqual(datetime.time(17, 0, 0), CourseJSONRetrieval.get_time(json_time))

    def test_get_location(self):
        location = TestCourseJSONRetrieval.get_test_location()
        self.assertEqual(location, CourseJSONRetrieval.get_location(self.meeting_json))

    def test_get_meeting(self):
        meeting = TestCourseJSONRetrieval.get_test_meeting()
        self.assertEqual(meeting, CourseJSONRetrieval.get_meeting(self.meeting_json))

    def test_get_course_identifier(self):
        identifier = TestCourseJSONRetrieval.get_test_course_identifier()
        self.assertEqual(identifier, CourseJSONRetrieval.get_course_identifier(self.course_json))

    def test_get_instructor(self):
        instructor = TestCourseJSONRetrieval.get_test_instructor()
        self.assertEqual(instructor, CourseJSONRetrieval.get_instructor(self.course_json['instructors'][0]))

    def test_get_registration_information(self):
        information = TestCourseJSONRetrieval.get_test_registration_information()
        self.assertEqual(information, CourseJSONRetrieval.get_registration_information(self.course_json))

    def test_get_enrollment_information(self):
        information = TestCourseJSONRetrieval.get_enrollment_information()
        self.assertEqual(information, CourseJSONRetrieval.get_enrollment_information(self.course_json))

    def test_get_instructor_set(self):
        instructors = {TestCourseJSONRetrieval.get_test_instructor()}
        self.assertEqual(instructors, CourseJSONRetrieval.get_instructor_set(self.course_json['instructors']))

    def test_get_meeting_set(self):
        meetings = {TestCourseJSONRetrieval.get_test_meeting()}
        self.assertEqual(meetings, CourseJSONRetrieval.get_meeting_set(self.course_json['meetings']))

    def test_get_empty_meeting_set(self):
        meetings = set()
        self.assertEqual(meetings, CourseJSONRetrieval.get_meeting_set(json.loads('[]')))

    def test_get_meeting_limited_information(self):
        with open(file_name_no_loc, 'r') as course_file:
            meetings = {TestCourseJSONRetrieval.get_test_meeting_limited_information()}
            course_json = json.loads(course_file.read())
            self.assertEqual(meetings, set(CourseJSONRetrieval.get_course(course_json).meeting.all()))

    def test_get_course(self):
        course = TestCourseJSONRetrieval.get_test_course()
        self.assertEqual(course, CourseJSONRetrieval.get_course(self.course_json))

    def test_get_course_set(self):
        course_list_json: json
        with open(file_name_list, 'r') as course_list_file:
            course_list_json = json.loads(course_list_file.read())
        course_set = CourseJSONRetrieval.get_course_set(course_list_json)
        self.assertEqual(100, len(course_set))
        self.assertTrue(TestCourseJSONRetrieval.get_test_course() in course_set)

    @staticmethod
    def get_test_course():
        course = Course.objects.create(
            course_identifier=TestCourseJSONRetrieval.get_test_course_identifier(),
            registration_information=TestCourseJSONRetrieval.get_test_registration_information(),
            enrollment_information=TestCourseJSONRetrieval.get_enrollment_information()
        )
        course.instructors.add(TestCourseJSONRetrieval.get_test_instructor())
        course.meeting.add(TestCourseJSONRetrieval.get_test_meeting())
        return course

    @staticmethod
    def get_test_registration_information():
        return RegistrationInformation.objects.create(
            class_number=16170,
            instruction_mode='P',
            instruction_mode_description='In Person',
            units='3',
            term='1238',
            component='LEC'
        )

    @staticmethod
    def get_test_instructor():
        return Instructor.objects.create(
            email='',
            name='To be Announced'
        )

    @staticmethod
    def get_test_course_identifier():
        return CourseIdentifier.objects.create(
            subject='CS',
            course_description='Introduction to Information Technology',
            catalog_number=1010
        )

    @staticmethod
    def get_test_location():
        return Location.objects.create(
            building='OLS',
            room='011',
            building_description='Olsson Hall 011'
        )

    @staticmethod
    def get_test_meeting():
        test_meeting = Meeting.objects.create(
            start_date=datetime.date(2023, 8, 22),
            end_date=datetime.date(2023, 12, 5),
            start_time=datetime.time(17, 0, 0),
            end_time=datetime.time(18, 15, 0),
            days='MoWe'
        )
        test_meeting.location.add(TestCourseJSONRetrieval.get_test_location().id)
        return test_meeting

    @staticmethod
    def get_test_meeting_limited_information():
        test_meeting = Meeting.objects.create(
            start_date=datetime.date(1996, 6, 11),
            end_date=datetime.date(1996, 8, 8),
            start_time=datetime.time(0, 0, 0),
            end_time=datetime.time(0, 0, 0),
            days='-'
        )
        test_meeting.location.add(
            Location.objects.create(
                building='-',
                building_description='-',
                room='-'
            ).id
        )
        return test_meeting

    @staticmethod
    def get_enrollment_information():
        return EnrollmentInformation.objects.create(
            waitlist_number=0,
            waitlist_capacity=199,
            class_capacity=75,
            enrollment_number=0,
            enrollment_capacity=75
        )
