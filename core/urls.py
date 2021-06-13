from django.urls import path, include
from  . import views


urlpatterns = [
    path('export-student/',  views.export_student, name='export-student'),
]
