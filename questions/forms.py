from django import forms
from questions.models import Datafile

# from .models import Question


# class QuestionForm(forms.Form):
#     CHOICES = [
#         ('1', 'True'),
#         ('2', 'False'),
#     ]
#     answer = forms.CharField(
#         label='',
#         widget=forms.RadioSelect(choices=CHOICES),
#     )
#     answer = forms.BooleanField()
#     class Meta:
#         model = Question
#         fields = ['answer']
class DatafileForm(forms.ModelForm):
    class Meta:
        model = Datafile
        fields = [
            "confidence_level",
            "test_stat",
            "ended",
            "document",
        ]
