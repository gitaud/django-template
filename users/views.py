from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

# Create your views here.
def home(request):
	return render(request, 'account/home.html', {'section': 'home'})

@login_required
def profile(request):
	return render(request, 'account/profile.html', {'user': request.user, 'section': 'profile'})

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			#Create a new user object but avoid saving it yet
			new_user = user_form.save(commit=False)
			#Set the chosen password
			new_user.set_password(
				user_form.cleaned_data['password']
			)
			#Save the user object
			new_user.save()
			authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'])
			login(request, new_user)
			return redirect(reverse('home'), 'account/home.html', {'section': 'home'})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'registration/register.html', {'user_form': user_form})