from django.shortcuts import render

from .models import Question

from .forms import QuestionForm

def question_view(request):
    form = QuestionForm(request.POST or None)
    # if form.is_valid():
        # form.save()
    context = {
        "form": form
    }
    return render(request,"questions/form.html", context)

# Create your views here.
