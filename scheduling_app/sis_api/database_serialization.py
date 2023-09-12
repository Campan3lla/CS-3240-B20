import django.core.serializers as ds

from scheduling_app.models import CourseIdentifier, Course, EnrollmentInformation, RegistrationInformation, Instructor, \
    Meeting, Location


def dump_data():
    courses = get_ten_courses_from_each_subject()
    all_courses = Course.objects.filter(id__in=map(lambda i: i.id, courses))
    all_identifiers = CourseIdentifier.objects.filter(id__in=map(lambda i: i.course_identifier.id, all_courses))
    all_enrollment_inf = EnrollmentInformation.objects.filter(
        id__in=map(lambda i: i.enrollment_information.id, all_courses))
    all_registration_inf = RegistrationInformation.objects.filter(
        id__in=map(lambda i: i.registration_information.id, all_courses))
    all_instructors = Instructor.objects.filter(
        id__in=map(lambda i: i.instructors.all().values_list('id', flat=True), all_courses))
    all_meetings = Meeting.objects.filter(id__in=map(lambda i: i.meeting.all().values_list('id', flat=True), all_courses))
    all_locations = Location.objects.filter(
        id__in=map(lambda i: i.location.all().values_list('id', flat=True), all_meetings))

    serialize_data = [
        *all_courses,
        *all_identifiers,
        *all_enrollment_inf,
        *all_registration_inf,
        *all_instructors,
        *all_meetings,
        *all_locations
    ]

    course_data = ds.serialize('json', serialize_data, indent=4)
    # identifier_data = ds.serialize('json', all_identifiers, indent=4)
    # enrollment_data = ds.serialize('json', all_enrollment_inf, indent=4)
    # registration_data = ds.serialize('json', all_registration_inf, indent=4)
    # meeting_data = ds.serialize('json', all_meetings, indent=4)
    # location_data = ds.serialize('json', all_locations, indent=4)
    # instructor_data = ds.serialize('json', all_instructors, indent=4)

    with open('dump_all.json', 'w') as out:
        out.writelines(
            course_data
        )


def get_ten_courses_from_each_subject():
    course_identifiers = CourseIdentifier.objects.filter().all()
    distinct_subjects = {*map(lambda i: i.subject, course_identifiers)}
    courses = []
    for subject in distinct_subjects:
        courses += Course.objects.filter(course_identifier__subject=subject)[:10]
    return courses
