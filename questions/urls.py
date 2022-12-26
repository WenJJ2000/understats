from django.contrib import admin
from django.urls import include, path
from questions.views import decision_tree_view

app_name = "questions"
urlpatterns = [
    # path('<int:id>/',decision_tree_view,name="decision_tree"),
    path('',decision_tree_view,name="decision_tree"),
]