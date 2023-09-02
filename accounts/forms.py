from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.core.mail import send_mail
from django.core.mail import mail_managers
from django.core.mail import mail_admins

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        send_mail(
                        subject='Добро пожаловать на наш новостной портал! ❤ Рита лучше всех ❤',
                        message=f'{user.username}, вы успешно зарегистрировались!',
                        from_email=None,
                        recipient_list=[user.email],
        )

        # mail_managers(
        #     subject='И снова поговорим о ❤',
        #     message=f'❤❤❤❤❤❤❤!'
        # )
        #
        # mail_admins(
        #     subject='Новый пользователь!',
        #     message=f'Пользователь {user.username} зарегистрировался на сайте.'
        # )

        return user

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )