from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

#https://blog.hlab.tech/part-ii-how-to-sign-up-user-and-send-confirmation-email-in-django-2-1-and-python-3-6/

class TokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
		)

account_activation_token = TokenGenerator()