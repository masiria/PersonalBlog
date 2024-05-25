from django.shortcuts import render
from django.views import View
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .forms import SignupForm
from .models import User
from.token import AccountActivationTokenGenerator


class RegisterView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            to = user.email
            subject = 'Activate Your Account'
            token = AccountActivationTokenGenerator.make_token(user)
            site = get_current_site(request)
            domain = site.domain
            uid = urlsafe_base64_encode(str(user.pk).encode())
            body = render_to_string('registration/activation_email.html',
                                    {
                                        'user': 'user',
                                        'token': token,
                                        'uid': uid,
                                        'domain': domain
                                    })
            email = EmailMessage(subject, body, to=[to])
            email.send()
            return render(request, 'registration/signup_thank.html')
        return render(request, 'registration/signup.html', {'form': form})


class ActivateView(View):
    def get(self, request, uid, token):
        uid = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(User, pk=uid)
        if user is not None and AccountActivationTokenGenerator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, 'registration/activation_failed.html')
