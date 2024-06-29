from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SignupForm


class SignupView(View):
    """Refactor the Signup view to be a class-based view"""
    form_class = SignupForm
    template = 'authentication/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # return redirect('home')
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template, {'form': form})
