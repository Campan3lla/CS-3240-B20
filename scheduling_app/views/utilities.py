from scheduling_app.models import Advisor, Student, StudentSchedule


def get_advisor_or_none(user):
    try:
        return Advisor.objects.get(related_user=user)
    except Advisor.DoesNotExist:
        return None


def get_student_or_none(user):
    try:
        return Student.objects.get(related_user=user)
    except Student.DoesNotExist:
        return None


def get_pending_schedules_or_none():  # get all pending schedules
    try:
        return StudentSchedule.objects.filter(status=StudentSchedule.Status.PENDING)
    except StudentSchedule.DoesNotExist:
        return None


def create_schedule_if_unique(user, schedule_name):
    _, created = create_schedule(user, schedule_name)
    if created:
        return {
            'title': 'Successfully Created Schedule',
            'body': 'You may now add courses to the schedule.'
        }
    else:
        return {
            'title': 'Error!',
            'body': 'You already have a schedule with that name.'
        }



def create_schedule(user, schedule_name):
    return StudentSchedule.objects.get_or_create(
        name=schedule_name,
        student_id=get_student_or_none(user).pk,
    )


def get_user_schedules(user):
    if student := get_student_or_none(user):
        return StudentSchedule.objects.filter(student_id=student.pk)
    else:
        return []
