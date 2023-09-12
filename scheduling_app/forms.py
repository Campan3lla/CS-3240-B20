from django import forms

from scheduling_app.models import User, Student, Advisor


class UserFormModel(forms.ModelForm):
    class Meta:
        model = User
        fields = ['account_type']
        

class StudentFormModel(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['related_user']


class AdvisorFormModel(forms.ModelForm):
    class Meta:
        model = Advisor
        fields = '__all__'
        exclude = ['related_user']