from django.shortcuts import render
from bj.models import CustomUser
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm

class SignupView(CreateView):
    model = CustomUser
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('bj:home')
