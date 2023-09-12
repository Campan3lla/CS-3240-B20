from django.shortcuts import render

from scheduling_app.authentication_decorators import unselected_account_type_required
from scheduling_app.views.utilities import get_advisor_or_none, get_student_or_none
from scheduling_app.authentication_decorators import is_student, is_advisor
from scheduling_app.forms import UserFormModel, StudentFormModel, AdvisorFormModel
from scheduling_app.models import Advisor, Student
from scheduling_app.views import student_schedules_view, advisor_schedules_view


def schedules_redirect_view(request):
    user = request.user
    if is_student(user):
        return student_schedules_view(request)
    elif is_advisor(user):
        return advisor_schedules_view(request)
    else:
        return login_view(request)


def login_view(request):
    user = request.user
    if user.is_authenticated and not is_student(user) and not is_advisor(user):
        return select_account_view(request)
    else:
        return render(request, 'scheduling_app/login.html')


@unselected_account_type_required()
def select_account_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserFormModel(request.POST)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            update_account(request, account_type, user)
            context = {
                'message': {
                    'title': 'Successfully entered account information.',
                    'body': 'You may now freely browse the site.'
                }
            }
            return render(request, 'scheduling_app/login.html', context)
    else:
        form = UserFormModel()
        student_form = StudentFormModel()
        advisor_form = AdvisorFormModel()
        context = {
            'form': form,
            'student_form': student_form,
            'advisor_form': advisor_form,
        }
        return render(request, 'scheduling_app/login-select-account.html', context)


def update_account(request, account_type, user):
    setattr(user, 'account_type', account_type)
    student_account = get_student_or_none(user)
    advisor_account = get_advisor_or_none(user)
    if account_type == 'student':
        update_student_user(advisor_account, request, student_account)
    elif account_type == 'advisor':
        update_advisor_account(advisor_account, request, student_account)
    user.save()


def update_advisor_account(advisor_account, request, student_account):
    if student_account:
        student_account.delete()
    advisor_form = AdvisorFormModel(request.POST)
    if advisor_form.is_valid():
        advisor_type = advisor_form.cleaned_data['advisor_type']
        if advisor_account:
            advisor_account.advisor_type = advisor_type
            advisor_account.save()
        else:
            Advisor.objects.create(related_user=request.user, advisor_type=advisor_type).save()


def update_student_user(advisor_account, request, student_account):
    if advisor_account:
        advisor_account.delete()
    student_form = StudentFormModel(request.POST)
    if student_form.is_valid():
        student_type = student_form.cleaned_data['student_type']
        if student_account:
            student_account.student_type = student_type
            student_account.save()
        else:
            Student.objects.create(related_user=request.user, student_type=student_type).save()
