from .views import ResumeView, CreateResumeView
from django.urls import path
from django.views.generic import RedirectView


urlpatterns = [
    path('resumes/', ResumeView.as_view(), name='resumes'),
    path('resume/new', CreateResumeView.as_view(), name='new_resume'),
    path('resume/new/', RedirectView.as_view(url='/resume/new'))
]
