from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import signals, authenticate, login
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sweet_alert.modal_alert import modal_message
from django.utils.datastructures import MultiValueDictKeyError


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            success_msg = "Your account has been created! You are now able to log in."
            messages.success(
                request, modal_message('success', None, success_msg))
            return redirect('login')
        else:
            messages.error(
                request, modal_message('error', None, "There's roblem while processing your registration.").display_message())
    else:
        form = UserRegisterForm()
    return render(request, 'authenticate/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            msg_error = ''
            user = authenticate(request, username=username, password=password)

            if user is not None:

                # no activation required
                login(request, user)
                return redirect('home')

                # add this line for email confirmation
                # if user.profile.is_confirm:
                #     login(request, user)
                #     return redirect('home')
                # else:
                #     msg_error = "Please activate your account. We send activation in your email"
                #     messages.error(
                #         request, modal_message('error', None, msg_error).display_message())
            else:
                msg_error = "Username and password didn't match"
                messages.error(
                    request, modal_message('error', None, msg_error).display_message())
        except MultiValueDictKeyError:
            msg_error = "There's a problem in login please try to login again."
            messages.error(
                request, modal_message('error', None, msg_error).display_message())

    return redirect('login')


@ login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, display_message(
                'success', None, 'Your profile has been updated'))
            return redirect(request.META['HTTP_REFERER'])
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


@ login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, display_message(
                'success', None, 'Your password was successfully updated!'))
            return redirect('users:profile')
        else:

            messages.error(request, display_message(
                'error', None, 'Please correct the error below'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):

    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        user = form.save()
        reset()
        return super().form_valid(form)


def login_summary(request):
    if request.method == 'GET':
        log_list = AccessLog.objects.filter(username=request.user)

        return render(request, 'users/access_logs.html', {'logs': logs_paginator(log_list, request)})


def login_summary_filter(request):
    if request.method == 'GET':
        attempt_time = request.GET['attempt_time']
        log_list = AccessLog.objects.filter(attempt_time__date=attempt_time)

        context = {
            'logs': logs_paginator(log_list, request),
            'filter_date': attempt_time,
        }
        return render(request, 'users/access_logs.html', context)


def logs_paginator(list, request):
    # paginator settings
    logs = None

    page = request.GET.get('page', 1)
    paginator = Paginator(list, 10)
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)

    return logs
