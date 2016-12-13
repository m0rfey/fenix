# -*- coding: utf-8 -*-

from django.contrib import auth, messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.core.mail import send_mail

from fenix import settings
from userprofile.forms import SignUpForm, SignInForm, EdirProfile
from userprofile.models import User

# Authentication
def signup(request):
    args={}
    args['title']= 'Sign Up'
    args.update(csrf(request))
    args['forms'] = SignUpForm()
    if request.POST:
        forms = SignUpForm(request.POST)
        if forms.is_valid():
            if not User.objects.filter(email=forms.cleaned_data['email']):
                forms.save()
                # Email message
                mess = 'Welcome, login: ' + request.POST.get('username', '') +\
                       ' Email: ' + request.POST.get('email', '') + \
                       ' Password:  ' + request.POST.get('password2', '')
                from_email = request.POST.get('email', '')
                send_mail('Welcome, you register site', mess, settings.EMAIL_HOST_USER, [from_email], fail_silently=False)

                # Authenticated
                login_new_user = auth.authenticate(username=forms.cleaned_data['username'],
                                                   password=forms.cleaned_data['password2'])
                auth.login(request, login_new_user)
                messages.success(request, "Регистрация произошла успешно. Если письмо о регистрации не пришло проверте папку СПАМ в почтовом ящике.", extra_tags="alert-success" )
                return redirect('/')
            else:
                messages.error(request, "Этот email уже кемто используется", extra_tags="alert-danger" )

    return render(request, '../templates/userprofile/signup.html', args)

def signin(request):
    args = {}
    args['title'] = 'Sign In'
    args.update(csrf(request))
    args['forms'] = SignInForm()
    if request.POST and ('pause', not request.session):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            request.session.set_expiry(15000)
            request.session['pause'] = True
            messages.success(request, "Поздравлаем %s, Вы успешно вошли " % auth.get_user(request).username, extra_tags="alert-success" )
            args['username'] = auth.get_user(request).username
            return redirect('/')
        else:
            messages.error(request, "Внимание! Не коректно введены данные", extra_tags="alert-danger" )
            return render(request, '../templates/userprofile/signin.html', args)
    else:
        return render(request, '../templates/userprofile/signin.html', args)

def signout(request):
    auth.logout(request)
    return_path = request.META.get('HTTP_REFERER', '/')

    return redirect(return_path)

# End Authentication

def profile(request, user_id):
    args={}
    args['title']= User.objects.get(id = user_id)
    try:
        args['user'] = User.objects.get(id=auth.get_user(request).id)
    except User.DoesNotExist:
        raise Http404
    args['username'] = auth.get_user(request).username
    return render(request, '../templates/userprofile/profile.html', args)

def edit_profile(request, user_id):
    args={}
    args.update(csrf(request))
    g =auth.get_user(request).username
    args['title'] = g
    args['username'] = g
    args['form'] = EdirProfile(instance= User.objects.get(id =auth.get_user(request).id))
    try:
        args['user'] =  User.objects.get(id=auth.get_user(request).id)
        if request.POST:
            new_user_form = EdirProfile(request.POST or None, request.FILES or None, instance=User.objects.get(id=auth.get_user(request).id))
            if new_user_form.is_valid():
                new_user_form.save()
                messages.success(request, "Изменения сохранены успешно", extra_tags="alert-success")
                return redirect('/user-%s/' % auth.get_user(request).id)
            else:
                messages.error(request, "Что-то пошло не так...", extra_tags="alert-danger")

    except User.DoesNotExist:
        raise Http404("DoesNotExist")

    return render(request, '../templates/userprofile/editprofile.html', args)