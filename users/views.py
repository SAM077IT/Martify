from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class Register(View):

    def get(self, request):
        register_form = SignUpForm()
        return render(request, "register.html", context={'register_form': register_form})

    def post(self, request):
        register_form = SignUpForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered successfully!"))
            return redirect('index')
        else:
            messages.success(request, ("Woops! registration failed!"))
            return render(request, "register.html", context={'register_form': register_form})


class Login(View):
    def get(self, request):
        return render(request, "login.html", context={})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have logged successfully!"))
            return redirect('index')
        else:
            messages.error(request, ("There is an error! please try again..."))
            return render(request, "login.html", context={})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, ("You have logged out successfully!"))
        return redirect('index')


class Dashboard(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'login'

    def get(self, request):
        return render(request, "dashboard.html", context={})
