from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.views.defaults import permission_denied
from .models import Vacancy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.decorators import method_decorator


# Create your views here.
class VacancyView(View):
    @staticmethod
    def get(request):
        vacancies = Vacancy.objects.all()
        return render(request, 'vacancies.html', context={'vacancies': vacancies})

    @staticmethod
    def home(request):
        return render(request, 'menu.html')


class SignupView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AuthLoginView(LoginView):
    template_name = 'login.html'


class AuthLogoutView(LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['description']


class CreateVacancyView(UserPassesTestMixin, View):
    template_name = 'create_vacancy.html'

    def test_func(self):
        return self.request.user.is_staff and self.request.user.is_authenticated

    @staticmethod
    def post(request):
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.author = request.user
            vacancy.save()
            return HttpResponse("Vacancy created successfully", status=302, headers={'Location': '/home'})
            # return redirect('home')
        else:
            print(form.errors)
            # return HttpResponseForbidden(status=403)
            return render(request, 'create_vacancy.html', {'form': form})

