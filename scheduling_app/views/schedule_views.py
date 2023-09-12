from django.shortcuts import render

from scheduling_app.authentication_decorators import student_required, advisor_required
from scheduling_app.models import StudentSchedule
from scheduling_app.views.utilities import get_pending_schedules_or_none, create_schedule_if_unique, get_user_schedules


def home_view(request):
    return render(request, 'scheduling_app/home.html')


@student_required()
def student_schedules_view(request):
    context = {}
    if request.method == 'POST':
        form = request.POST
        if 'delete_course_form' in form:
            course_pk = int(form['course_pk'])
            schedule_pk = int(form['schedule_pk'])
            schedule = StudentSchedule.objects.get(pk=schedule_pk)
            schedule.courses.remove(course_pk)
            schedule.save()
        elif 'edit_schedule_status_form' in form:
            schedule_pk = int(form['schedule_pk'])
            schedule = StudentSchedule.objects.get(pk=schedule_pk)
            if 'submit' in form:
                schedule.status = StudentSchedule.Status.PENDING
                schedule.save()
            elif 'withdraw' in form:
                schedule.status = StudentSchedule.Status.NOT_SUBMITTED
                schedule.save()
            elif 'delete' in form:
                schedule.delete()
        elif 'create_schedule_form' in form:
            context['message'] = create_schedule_if_unique(request.user, form['schedule_name'])

    sort_order = {
        StudentSchedule.Status.APPROVED.__str__(): 1,
        StudentSchedule.Status.REJECTED.__str__(): 2,
        StudentSchedule.Status.PENDING.__str__(): 3,
        StudentSchedule.Status.NOT_SUBMITTED.__str__(): 4,
    }

    context['schedules'] = sorted(
            get_user_schedules(request.user),
            key=lambda i: sort_order[i.status.__str__()]
        )
    return render(request, 'scheduling_app/student-schedule-table.html', context=context)


@advisor_required()
def advisor_schedules_view(request):
    if request.method == 'POST':
        form = request.POST
        if 'edit_schedule_status_form' in form:
            schedule_pk = int(form['schedule_pk'])
            schedule = StudentSchedule.objects.get(pk=schedule_pk)
            if 'approve' in form:
                schedule.status = StudentSchedule.Status.APPROVED
                schedule.save()
            elif 'reject' in form:
                schedule.status = StudentSchedule.Status.REJECTED
                schedule.save()
    context = {
        'schedules': get_pending_schedules_or_none()
    }
    return render(request, 'scheduling_app/advisor-schedule-table.html', context)


