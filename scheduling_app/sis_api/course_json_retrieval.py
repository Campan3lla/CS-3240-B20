import datetime
import json
import re
from scheduling_app.models import CourseIdentifier, Course, Location, Instructor, Meeting, RegistrationInformation, \
    EnrollmentInformation


class CourseJSONRetrieval:
    @staticmethod
    def get_course_identifier(course_json: json):
        return CourseIdentifier.objects.get_or_create(
            subject=course_json['acad_org'],
            catalog_number=int(course_json['catalog_nbr']),
            course_description=course_json['descr']
        )[0]

    @staticmethod
    def get_location(meeting_json: json):
        def get_or_default(key, default):
            return meeting_json[key] if key in meeting_json else default

        return Location.objects.get_or_create(
            building=get_or_default('bldg_cd', '-'),
            room=get_or_default('room', '-'),
            building_description=get_or_default('facility_descr', '-')
        )[0]

    @staticmethod
    def get_time(raw_time_str):
        matches = re.match('[^\d]*(?P<hour>\d+).(?P<minute>\d+).(?P<second>\d+)', raw_time_str)
        if matches is None:
            return datetime.time(0, 0, 0)
        else:
            data = matches.groupdict()
            return datetime.time(int(data['hour']), int(data['minute']), int(data['second']))

    @staticmethod
    def get_date(raw_date_str):
        matches = re.match('[^\d]*(?P<month>\d+).(?P<day>\d+).(?P<year>\d+)', raw_date_str)
        if matches is None:
            return datetime.date(1, 1, 1)
        else:
            data = matches.groupdict()
            return datetime.date(int(data['year']), int(data['month']), int(data['day']))

    @staticmethod
    def get_meeting(meeting_json: json):
        def get_or_default(key, value, default):
            return value if key in meeting_json else default

        meeting = Meeting.objects.get_or_create(
            days=get_or_default(
                'days',
                meeting_json['days'],
                '-'
            ),
            start_date=get_or_default(
                'start_dt',
                CourseJSONRetrieval.get_date(meeting_json['start_dt']),
                datetime.date(1, 1, 1)
            ),
            end_date=get_or_default(
                'end_dt',
                CourseJSONRetrieval.get_date(meeting_json['end_dt']),
                datetime.date(1, 1, 1)
            ),
            start_time=get_or_default(
                'start_time',
                CourseJSONRetrieval.get_time(meeting_json['start_time']),
                '00:00:00'),
            end_time=get_or_default(
                'end_time',
                CourseJSONRetrieval.get_time(meeting_json['end_time']),
                '00:00:00'
            )
        )[0]
        meeting.location.add(CourseJSONRetrieval.get_location(meeting_json).id)
        return meeting

    @staticmethod
    def get_instructor(instructor_json: json):
        return Instructor.objects.get_or_create(
            name=instructor_json['name'],
            email=instructor_json['email']
        )[0]

    @staticmethod
    def get_instructor_set(instructors_json: json):
        instructors = set()
        for instructor_json in instructors_json:
            instructors.add(CourseJSONRetrieval.get_instructor(instructor_json))
        return instructors

    @staticmethod
    def get_meeting_set(meetings_json: json):
        meetings = set()
        for meeting_json in meetings_json:
            meetings.add(CourseJSONRetrieval.get_meeting(meeting_json))
        return meetings

    @staticmethod
    def get_registration_information(course_json: json):
        return RegistrationInformation.objects.create(
            term=course_json['strm'],
            class_number=course_json['class_nbr'],
            units=course_json['units'],
            instruction_mode_description=course_json['instruction_mode_descr'],
            instruction_mode=course_json['instruction_mode'],
            component=course_json['component']
        )

    @staticmethod
    def get_enrollment_information(course_json: json):
        return EnrollmentInformation.objects.create(
            enrollment_number=course_json['enrollment_total'],
            enrollment_capacity=course_json['enrollment_available'],
            waitlist_number=course_json['wait_tot'],
            waitlist_capacity=course_json['wait_cap'],
            class_capacity=course_json['class_capacity']
        )

    @staticmethod
    def get_course(course_json: json):
        course = Course.objects.get_or_create(
            course_identifier=CourseJSONRetrieval.get_course_identifier(course_json),
            registration_information=CourseJSONRetrieval.get_registration_information(course_json),
            enrollment_information=CourseJSONRetrieval.get_enrollment_information(course_json)
        )[0]
        instructors = CourseJSONRetrieval.get_instructor_set(course_json['instructors'])
        meetings = CourseJSONRetrieval.get_meeting_set(course_json['meetings'])
        course.instructors.add(*[instructor.id for instructor in instructors])
        course.meeting.add(*[meeting.id for meeting in meetings])
        return course

    @staticmethod
    def get_course_set(course_list_json: json):
        course_set = set()
        for course_json in course_list_json:
            course_set.add(CourseJSONRetrieval.get_course(course_json))
        return course_set
