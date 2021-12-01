from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model

from .token import account_activation_token
from .forms import UserRegistrationForm

UserProfile = get_user_model()

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
			new_user.is_active = False
			new_user.save()
			current_site = get_current_site(request)
			email_subject = 'Activate Your Account'
			message = render_to_string('registration/activate_account.html', {
				'user': new_user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
				'token': account_activation_token.make_token(new_user)
			})
			to_email = user_form.cleaned_data['email']
			email = EmailMessage(email_subject, message, to=[to_email])
			email.send()
			#authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'])
			#login(request, new_user)
			#return redirect(reverse('home'), 'account/home.html', {'section': 'home'})
			return render(request, 'registration/register_done.html', {'user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'registration/register.html', {'user_form': user_form})

def activate_account(request, uidb64, token):
	try:
		uid = force_bytes(urlsafe_base64_decode(uidb64))
		user = UserProfile.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return render(request, 'registration/register_complete.html', {'section': 'home', 'user': user})
	else:
		return render(request, 'registration/register_complete.html', {'section': 'home'})