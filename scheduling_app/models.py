import enum
import re

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

import hashlib

from schedule_advisor import settings


# Create your models here.


# https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
class User(AbstractUser):
    ACCOUNT_TYPES = (
        ('student', 'Student'),
        ('advisor', 'Advisor'),
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)


# abstract class for query, referenced following:
# https://www.geeksforgeeks.org/how-to-create-abstract-model-class-in-django/
class Student(models.Model):
    related_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='student_account',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    STUDENT_TYPES = (
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
    )
    student_type = models.CharField(
        max_length=20,
        choices=STUDENT_TYPES,
    )


class Advisor(models.Model):
    related_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='advisor_account',
        on_delete=models.CASCADE,
        primary_key=True)
    ADVISOR_TYPES = (
        ('undergraduate', 'Undergraduate Advisor'),
        ('graduate', 'Graduate Advisor'),
    )
    advisor_type = models.CharField(
        max_length=20,
        choices=ADVISOR_TYPES,
    )


class Location(models.Model):
    building = models.CharField(max_length=64)
    room = models.CharField(max_length=32)
    building_description = models.CharField(max_length=96)

    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        else:
            return (
                    self.room == other.room and
                    self.building_description == other.building_description and
                    self.building == other.building
            )

    def __str__(self):
        return f"{self.room} {self.building_description} {self.building}"

    def __hash__(self):
        # Hash the string representation of the object using the SHA-256 algorithm
        hash_object = hashlib.sha256(str(self).encode('utf-8'))
        # Return the hash value of the hexadecimal string
        return int(hash_object.hexdigest(), 16)


class Days(enum.Enum):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'


class Meeting(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.ManyToManyField(Location)
    days = models.CharField(max_length=32)

    @staticmethod
    def __conflict(start1, start2, end1, end2):
        return max(start1, start2) <= min(end1, end2)

    def overlapping_times(self, other):
        start_time1 = self.start_time
        end_time1 = self.end_time
        start_time2 = other.start_time
        end_time2 = other.end_time
        return self.__conflict(start_time1, start_time2, end_time1, end_time2)

    def overlapping_dates(self, other):
        start_date1 = self.start_date
        end_date1 = self.end_date
        start_date2 = other.start_date
        end_date2 = other.end_date
        return self.__conflict(start_date1, start_date2, end_date1, end_date2)

    def get_day_set(self):
        pattern = r'''
        (?:(?P<Monday>Mo?)[,\s]?)?
        (?:(?P<Tuesday>T(?!h)u?)[,\s]?)?
        (?:(?P<Wednesday>We?)[,\s]?)?
        (?:(?P<Thursday>[TR](?!u|,)h?)[,\s]?)?
        (?:(?P<Friday>Fr?)[,\s]?)?
        (?:(?P<Saturday>S(?!u)a?)[,\s]?)?
        (?:(?P<Sunday>S(?!a)u?)[,\s]?)?
        '''
        regex = re.compile(pattern, re.VERBOSE)
        day_set = set()
        for match in re.finditer(regex, self.days):
            day_set |= set(day for day in Days if match.group(day.value))
        return day_set

    def overlapping_days(self, other):
        return bool(self.get_day_set() & other.get_day_set())

    def overlaps(self, other):
        return self.overlapping_days(other) and self.overlapping_days(other) and self.overlapping_times(other)

    def __eq__(self, other):
        if not isinstance(other, Meeting):
            return False
        else:
            return (
                    self.start_time == other.start_time and
                    self.end_time == other.end_time and
                    self.start_date == other.start_date and
                    self.end_date == other.end_date and
                    self.days == other.days and
                    set(self.location.all()) == set(other.location.all())
            )

    def __str__(self):
        return f"{self.start_date} {self.end_date} " \
               f"{self.start_time} {self.end_time} " \
               f"{self.days} {str(set(self.location.all()))}"

    def __hash__(self):
        # Hash the string representation of the object using the SHA-256 algorithm
        hash_object = hashlib.sha256(str(self).encode('utf-8'))
        # Return the hash value of the hexadecimal string
        return int(hash_object.hexdigest(), 16)


class CourseIdentifier(models.Model):
    subject = models.CharField(max_length=32)
    catalog_number = models.IntegerField()
    course_description = models.CharField(max_length=256)

    def __eq__(self, other):
        if not isinstance(other, CourseIdentifier):
            return False
        else:
            return (
                    self.subject == other.subject and
                    self.catalog_number == other.catalog_number and
                    self.course_description == other.course_description
            )

    def __str__(self):
        return f"{self.subject} {self.catalog_number} {self.course_description}"

    def __hash__(self):
        hash_object = hashlib.sha256(str(self).encode('utf-8'))
        return int(hash_object.hexdigest(), 16)


class Instructor(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)

    def __eq__(self, other):
        if not isinstance(other, Instructor):
            return False
        else:
            return (
                    self.name == other.name and
                    self.email == other.email
            )

    def __str__(self):
        return f"{self.name} {self.email}"

    def __hash__(self):
        hash_object = hashlib.sha256(str(self).encode('utf-8'))
        return int(hash_object.hexdigest(), 16)


class RegistrationInformation(models.Model):
    class_number = models.IntegerField()
    instruction_mode = models.CharField(max_length=32)
    instruction_mode_description = models.CharField(max_length=32)
    units = models.CharField(max_length=16)
    term = models.CharField(max_length=16)
    component = models.CharField(max_length=16)

    def __eq__(self, other):
        if not isinstance(other, RegistrationInformation):
            return False
        else:
            return (
                    self.class_number == other.class_number and
                    self.instruction_mode == other.instruction_mode and
                    self.instruction_mode_description == other.instruction_mode_description and
                    self.units == other.units and
                    self.term == other.term and
                    self.component == other.component
            )

    def __str__(self):
        return f"{self.class_number} " \
               f"{self.component} {self.instruction_mode} {self.instruction_mode_description} " \
               f"{self.units} {self.term}"

    def __hash__(self):
        hash_object = hashlib.sha256(str(self).encode('utf-8'))
        return int(hash_object.hexdigest(), 16)


class EnrollmentInformation(models.Model):
    waitlist_number = models.IntegerField()
    waitlist_capacity = models.IntegerField()
    class_capacity = models.IntegerField()
    enrollment_number = models.IntegerField()
    enrollment_capacity = models.IntegerField()

    def __eq__(self, other):
        if not isinstance(other, EnrollmentInformation):
            return False
        else:
            return (
                    self.enrollment_number == other.enrollment_number and
                    self.enrollment_capacity == other.enrollment_capacity and
                    self.class_capacity == other.class_capacity and
                    self.waitlist_number == other.waitlist_number and
                    self.waitlist_capacity == other.waitlist_capacity
            )

    def __str__(self):
        return f"{self.enrollment_number} {self.enrollment_capacity} " \
               f"{self.waitlist_number} {self.enrollment_capacity} " \
               f"{self.class_capacity}"

    def __hash__(self):
        hash_object = hashlib.sha256(str(self).encode('utf-8'))
        return int(hash_object.hexdigest(), 16)


class Course(models.Model):
    course_identifier = models.ForeignKey(CourseIdentifier, on_delete=models.CASCADE)
    meeting = models.ManyToManyField(Meeting)
    instructors = models.ManyToManyField(Instructor)
    registration_information = models.OneToOneField(RegistrationInformation, on_delete=models.CASCADE)
    enrollment_information = models.OneToOneField(EnrollmentInformation, on_delete=models.CASCADE)

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        else:
            return (
                    self.course_identifier == other.course_identifier and
                    self.registration_information == other.registration_information and
                    self.enrollment_information == other.enrollment_information and
                    set(self.meeting.all()) == set(other.meeting.all()) and
                    set(self.instructors.all()) == set(other.instructors.all())
            )

    def __str__(self):
        return f"{self.course_identifier} {set(self.meeting.all())} " \
               f"{set(self.instructors.all())} {self.registration_information} {self.enrollment_information}"

    def __hash__(self):
        hash_object = hashlib.sha256(str(self).encode('utf-8'))
        return int(hash_object.hexdigest(), 16)


class StudentSchedule(models.Model):
    student = models.ForeignKey(Student, related_name='created_by_student', on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, related_name='scheduled_course')
    name = models.CharField(max_length=64, blank=False, validators=[MinLengthValidator(1)])

    class Status(enum.Enum):
        NOT_SUBMITTED = 'Not Submitted'
        PENDING = 'Pending'
        APPROVED = 'Approved'
        REJECTED = 'Rejected'

    status = models.CharField(
        max_length=32,
        choices=[(enum, enum.value) for enum in Status],
        default=f'{Status.NOT_SUBMITTED}'
    )
    def overlaps(self, course: Course):
        schedule_meetings = [meeting for course in self.courses.all() for meeting in course.meeting.all()]
        course_meetings = course.meeting.all()
        return any(
            course_meeting.overlaps(schedule_meeting)
            for course_meeting in course_meetings
            for schedule_meeting in schedule_meetings
        )

    def has_course(self, course: Course):
        return course in self.courses.all()
