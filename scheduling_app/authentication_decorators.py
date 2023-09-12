from django.contrib.auth.decorators import user_passes_test


#https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
def student_required(function=None, redirect_field_name='redirect_from', redirect_url='scheduling_app:login'):
    """
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and is_student(u),
        login_url=redirect_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(function) if function else actual_decorator


def advisor_required(function=None, redirect_field_name='redirect_from', redirect_url='scheduling_app:login'):
    """
    Decorator for views that checks that the logged-in user is an advisor,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and is_advisor(u),
        login_url=redirect_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(function) if function else actual_decorator

def account_type_required(function=None, redirect_field_name='redirect_from', redirect_url='scheduling_app:login'):
    """
    Decorator for views that checks that the logged-in user has an account type,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and is_student(u) or is_advisor(u),
        login_url=redirect_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(function) if function else actual_decorator

def unselected_account_type_required(function=None, redirect_field_name='redirect_from', redirect_url='scheduling_app:login'):
    """
    Decorator for views that checks that the logged-in user has an account type,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not is_student(u) and not is_advisor(u) and not u.is_anonymous,
        login_url=redirect_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(function) if function else actual_decorator

def admin_required(function=None, redirect_field_name='redirect_from', redirect_url='scheduling_app:login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=redirect_url,
        redirect_field_name=redirect_field_name
    )
    return actual_decorator(function) if function else actual_decorator

def is_student(user):
    if hasattr(user, 'account_type'):
        return user.account_type == 'student'
    else:
        return False


def is_advisor(user):
    if hasattr(user, 'account_type'):
        return user.account_type == 'advisor'
    else:
        return False
