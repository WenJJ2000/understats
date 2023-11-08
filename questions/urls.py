from django.contrib import admin
from django.urls import include, path
from questions.views import decision_tree_view, show_result, upload_file

app_name = "questions"
urlpatterns = [
    # path('<int:id>/',decision_tree_view,name="decision_tree"),
    path("", decision_tree_view, name="Decisions"),
    # path("UploadFile", upload_file, name="UploadFile"),
    path("Result", show_result, name="ShowResults"),
]
