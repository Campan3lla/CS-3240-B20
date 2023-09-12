from django.shortcuts import render

from scheduling_app.authentication_decorators import admin_required


@admin_required()
def testing_page(request):
    return render(request, 'scheduling_app/testing_page.html')