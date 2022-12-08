from django.contrib import admin
from django.urls import include, path
from questions.views import question_view

app_name = "questions"
urlpatterns = [
    path('',question_view,name="question-list"),
]