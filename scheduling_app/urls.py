from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'scheduling_app'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/login', views.account_views.login_view, name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/select-account', views.account_views.select_account_view, name='accountSelect'),
    path('account/redirect-schedules', views.account_views.schedules_redirect_view, name='accountRedirects'),
    path('courses', views.course_view.course_table_view, name='courseTable'),
    path('schedules/student', views.student_schedules_view, name='studentSchedules'),
    path('schedules/advisor', views.advisor_schedules_view, name='advisorSchedules'),

    path('admin/testing-page', views.testing_page, name='testingPage')
]