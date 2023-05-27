from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Resume
from django import forms
from django.contrib.auth.decorators import login_required


# Create your views here.
class ResumeView(View):
    @staticmethod
    def get(request):
        resumes = Resume.objects.all()
        return render(request, 'resume.html', context={'resumes': resumes})


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['description']


class CreateResumeView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_staff

    @staticmethod
    @login_required()
    def post(request):
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.author = request.user
            resume.save()
            return redirect('home')
        else:
            return render(request, 'create_resume.html', {'form': form})
