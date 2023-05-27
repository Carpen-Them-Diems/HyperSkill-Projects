from .views import VacancyView, SignupView, AuthLoginView, AuthLogoutView, CreateVacancyView
from django.urls import path
from django.views.generic import RedirectView


urlpatterns = [
    path('vacancies/', VacancyView.as_view(), name='vacancies'),
    path('home/', VacancyView.home, name='home'),
    path('login', AuthLoginView.as_view(), name='login'),
    path('logout', AuthLogoutView.as_view(), name='logout'),
    path('signup', SignupView.as_view(), name='signup'),
    path('login/', RedirectView.as_view(url='/login')),
    path('logout/', RedirectView.as_view(url='/logout')),
    path('signup/', RedirectView.as_view(url='/signup')),
    path('vacancy/new/', CreateVacancyView.as_view(), name='new_vacancy'),
]
