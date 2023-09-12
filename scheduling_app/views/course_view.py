from django.shortcuts import render

from scheduling_app.authentication_decorators import account_type_required
from scheduling_app.models import StudentSchedule, Course
from scheduling_app.sis_api import By, Semester
from scheduling_app.sis_api.populate_database import fill_database_by_query
from scheduling_app.views.utilities import create_schedule_if_unique, get_user_schedules


@account_type_required()
def course_table_view(request):
    if request.method == 'POST':
        form = request.POST
        if 'filter_form' in form:
            return course_table_filter_form(form, request)
        elif 'create_schedule_form' in form:
            return course_table_create_schedule_form(form, request)
        elif 'add_course_to_schedule_form' in form:
            return course_table_add_course_to_schedule_form(form, request)
    return course_table_base_page(request)


def course_table_base_page(request):
    context = {
        'courses': [],
        'schedules': get_user_schedules(request.user)
    }
    return render(request, 'scheduling_app/course-table.html', context=context)


def course_table_add_course_to_schedule_form(form, request):
    print(form)
    student_schedule = StudentSchedule.objects.get(pk=int(form['add_schedule']))
    course = Course.objects.get(pk=int(form['add_course']))
    context = {
        'courses': [],
        'schedules': get_user_schedules(request.user)
    }
    if student_schedule.has_course(course):
        context['message'] = {
            'title': 'Error!',
            'body': 'The selected course is already within the schedule.'
        }
    elif student_schedule.overlaps(course):
        context['message'] = {
                'title': 'Error!',
                'body': 'The selected courses conflict. Please select a different course.'
            }
    else:
        student_schedule.courses.add(course.pk)
        context['message'] = {
            'title': 'Success!',
            'body': f'"{course.course_identifier.course_description}" was successfully added to "{student_schedule.name}"'
        }
    print(request)
    return render(request, 'scheduling_app/course-table.html', context=context)


def course_table_create_schedule_form(form, request):
    context = {
        'courses': [],
        'message': create_schedule_if_unique(request.user, form['schedule_name']),
        'schedules': get_user_schedules(request.user)
    }
    return render(request, 'scheduling_app/course-table.html', context=context)


def course_table_filter_form(form, request):
    kwargs = {}
    course_filter = [By.term(2023, Semester.SUMMER)]
    if form['subject']:
        kwargs['course_identifier__subject__icontains'] = form['subject']
        course_filter.append(By.subject(form['subject']))
    if form['catalog_number']:
        kwargs['course_identifier__catalog_number'] = form['catalog_number']
        course_filter.append(By.catalog_number(form['catalog_number']))
    if form['class_number']:
        kwargs['registration_information__class_number'] = form['class_number']
        course_filter.append(By.class_number(form['class_number']))
    if form['professor']:
        kwargs['instructors__name__icontains'] = form['professor']
        course_filter.append(By.instructor(form['professor']))
    if form['keyword']:
        kwargs['course_identifier__course_description__icontains'] = form['keyword']
        course_filter.append(By.keyword(form['keyword']))
    courses = Course.objects.all().filter(**kwargs)

    if not courses:
        courses = fill_database_by_query(*course_filter)
        print("Course not found in database")
    else:
        print("Course was found in database")
    context = {
        'courses': courses,
        'schedules': get_user_schedules(request.user)
    }
    return render(request, 'scheduling_app/course-table.html', context=context)
