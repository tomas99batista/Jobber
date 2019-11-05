from django.urls import path

from job_app import views
from jobber import settings
from .views import *
from django.conf.urls.static import static
import django.contrib.staticfiles
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

urlpatterns = [
    path('', views.search_job, name='index'),
    path('job_list/', joblistview,name='job_list'),
    path('job_create/', jobcreateview, name="job_create"),
]