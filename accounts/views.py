from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash, login
from django.contrib.auth.backends import UserModel
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, INTERNAL_RESET_SESSION_TOKEN
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, UpdateView, FormView, RedirectView  # ,ListView, DetailView, CreateView, DeleteView

from dm_apps.utils import custom_send_mail
from . import emails
from . import forms
from . import models
from .auth_helper import get_sign_in_url, get_token_from_code, remove_user_and_token
from .graph_helper import get_user
from .tokens import account_activation_token


def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)

    # Get the user's profile
    user = get_user(token)
    my_email = user.get("mail") if user.get("mail") else user.get("userPrincipalName")
    my_first_name = user.get("givenName")
    my_last_name = user.get("surname")
    my_job = user.get("jobTitle")
    my_phone = user.get("businessPhones")

    try:
        my_user = User.objects.get(email__iexact=my_email)
        my_user.first_name = my_first_name
        my_user.last_name = my_last_name
        my_user.save()
    except User.DoesNotExist:
        my_user = User.objects.create(
            username=my_email,
            email=my_email,
            first_name=my_first_name,
            last_name=my_last_name,
            is_active=True,
            password="pbkdf2_sha256$120000$ctoBiOUIJMD1$DWVtEKBlDXXHKfy/0wKCpcIDYjRrKfV/wpYMHKVrasw=",
        )
    finally:
        my_profile = my_user.profile
        my_profile.position_eng = my_job
        my_profile.position_fre = my_job
        my_profile.phone = my_phone
        try:
            my_profile.save()
        except:
            print("there was an error in trying to copy over the user's profile data from AAD")

    login(request, my_user)
    return HttpResponseRedirect(reverse('index'))


class CloserTemplateView(TemplateView):
    template_name = 'accounts/close_me.html'


# This is a good one. It should be able to replace all others with the message arg.
def access_denied(request, message=None):
    my_url = reverse("accounts:request_access")
    a_tag = mark_safe(
        '<a pop-href="{}" href="#" class="btn btn-sm btn-primary badge request-access-button">{}</a>'.format(my_url, _("Request access")))
    if not message:
        message = _("Sorry, you are not authorized to view this page.")
    denied_message = "{} {}".format(message, a_tag)
    messages.error(request, mark_safe(denied_message))
    # send user back to the page that they came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProfileUpdateView(UpdateView):
    model = models.Profile
    form_class = forms.ProfileForm
    success_url = "#"

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs['pk'])
        try:
            profile = models.Profile.objects.get(user=user)
        except models.Profile.DoesNotExist:
            print("Profile does not exist, creating Profile")
            profile = models.Profile(user=user)

        return profile

    def form_valid(self, form):
        messages.success(self.request, _("Successfully updated!"))
        return super().form_valid(form)


class UserLoginView(PasswordResetView):
    template_name = "registration/login.html"
    form_class = forms.DMAppsEmailLoginForm
    from_email = settings.SITE_FROM_EMAIL
    subject_template_name = 'registration/dm_apps_email_login_subject.txt'
    email_template_name = 'registration/dm_apps_email_login_email.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if settings.AZURE_AD:
            return HttpResponseRedirect(reverse("accounts:azure_login"))
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        messages.success(self.request, f'<span class="mdi mdi-email-outline mr-3 lead"></span>' + _("An e-mail with a login link has been sent to you!"))
        return reverse('index')


class CallBack(RedirectView):
    token_generator = default_token_generator
    reset_url_token = 'cleared'
    url = reverse_lazy("index")
    invalid_token_msg = gettext_lazy("Sorry the link you used to sign in with is not valid!")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        # this gets the using based on the encrypted pk
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']

            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    self.user.is_active = True
                    self.user.save()
                    login(self.request, self.user)
                else:
                    messages.error(self.request, self.invalid_token_msg)

            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)
                else:
                    messages.error(self.request, self.invalid_token_msg)
            return super().dispatch(*args, **kwargs)
        else:
            messages.error(self.request, self.invalid_token_msg)
        return super().dispatch(*args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        remove_user_and_token(request)
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = forms.UserAccountForm
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object.username = self.object.email
        return super().form_valid(form)


def change_password(request):
    # user_model = get_user_model()
    # print(user_model.id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def account_verified(request):
    group = Group.objects.get(name='verified')
    if group in request.user.groups.all():
        messages.error(request, 'This account has already been verified')
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SetPasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!

                # the user should be added to the People object of data inventory
                # user_instance = User.objects.get(pk=user.id) #for some reason, the create() method does not want to accept the user instance
                # new_person = inventory_models.Person.objects.create(
                #     user=user_instance,
                #     full_name="{}, {}".format(user.last_name, user.first_name),
                #     organization_id=6
                # )
                user.groups.add(group)

                messages.success(request, 'Your password was successfully updated!')
                return redirect('index')
        else:
            form = SetPasswordForm(request.user)
        return render(request, 'registration/account_verified.html', {
            'form': form
        })


def resend_verification_email(request, email):
    group = Group.objects.get(name='verified')
    user = User.objects.get(email__iexact=email)
    try:
        user.groups.remove(group)
    except:
        pass
    current_site = get_current_site(request)
    mail_subject = 'Activate your Gulf Region Data Management account.'
    message = render_to_string('registration/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    from_email = settings.SITE_FROM_EMAIL
    custom_send_mail(
        subject=mail_subject,
        html_message=message,
        from_email=from_email,
        recipient_list=to_email,
    )

    return HttpResponse('A verification email has been sent. Please check your inbox.')


def signup(request):
    if request.method == 'POST':
        form = forms.UserAccountForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your DM Apps account / Activez votre compte Applications GD'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            print(to_email)
            from_email = settings.SITE_FROM_EMAIL
            custom_send_mail(
                html_message=message,
                subject=mail_subject,
                recipient_list=[to_email, ],
                from_email=from_email,
            )
            messages.success(request, _('A verification email was just send to {email_address}. In order to complete your registration, please follow the link'
                                  ' in the message. <br><br>If the email does not appear within 1-2 minutes, please be sure to check your junk mail folder. '
                                  '<br><br>The activation link will only remain valid for a limited period of time.').format(email_address=to_email))
            return HttpResponseRedirect(reverse('index'))
    else:
        form = forms.UserAccountForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        messages.success(request, 'Congrats! Your account has been successfully verified')
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Activation link is invalid!')


class UserPassWordResetView(PasswordResetView):
    template_name = "registration/user_password_reset_form.html"
    success_message = "An email has been sent!"
    form_class = forms.DMAppsPasswordResetForm
    from_email = settings.SITE_FROM_EMAIL
    subject_template_name = 'registration/dm_apps_password_reset_subject.txt'
    email_template_name = 'registration/dm_apps_password_reset_email.html'
    success_url = reverse_lazy('index')

    def get_success_url(self, **kwargs):
        messages.success(self.request, self.success_message)
        return reverse('index')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/user_password_reset_confirm.html"

    def get_success_url(self, **kwargs):
        messages.success(self.request,
                         "Your password has been successfully reset! Please try logging in with your new password.")
        return reverse('index')

    def form_valid(self, form):
        super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class RequestAccessFormView(LoginRequiredMixin, FormView):
    template_name = "accounts/request_access_form_popout.html"
    form_class = forms.RequestAccessForm

    def get_initial(self):
        user = self.request.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'user_id': user.id,
        }

    def form_valid(self, form):
        context = {
            "first_name": form.cleaned_data["first_name"],
            "last_name": form.cleaned_data["last_name"],
            "email": form.cleaned_data["email"],
            "user_id": form.cleaned_data["user_id"],
            "application": form.cleaned_data["application"],
            "optional_comment": form.cleaned_data["optional_comment"],
        }
        email = emails.RequestAccessEmail(context, self.request)
        # send the email object
        custom_send_mail(
            subject=email.subject,
            html_message=email.message,
            from_email=email.from_email,
            recipient_list=email.to_list
        )
        messages.success(self.request,
                         message="your request has been sent to the site administrator")
        return HttpResponseRedirect(reverse('accounts:close_me'))
