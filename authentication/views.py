from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginUserForm
from django.views import View
from .models import UserProfile

class CreateUser(View):
    template_name = 'registration/create_user.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Save the user object
            user = form.save()
            # Optionally, you can associate the UserProfile with the user here
            # For example:
            # UserProfile.objects.create(user=user, additional_field='value')

            return redirect('login')

        return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'registration/login_user.html' 
    def get(self, request):
        form = LoginUserForm()
        return render(request, self.template_name , {'form': form})
    