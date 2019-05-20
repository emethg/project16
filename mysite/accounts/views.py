from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, UserProfile, SportActivityNotification, SportActivity
from django.contrib.auth.views import LoginView

from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# hello
from webpush import send_user_notification

from .models import Todo
from .forms import TodoForm

import json

from celery.schedules import crontab
from celery.task import periodic_task


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


@login_required()
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


@login_required()
def view_items(request):
    '''
    views for item list
    '''
    # test jira
    data = Product.objects.all().order_by('?')
    args = {'data': data}
    return render(request, 'accounts/items_list.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('/accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            redirect('/account/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


@periodic_task(run_every=crontab())
def send_push(request):
    profile = request.user.get_profile()
    if profile.notification == 'True':
        try:
            body = request.body
            data = json.loads(body)

            if 'head' not in data or 'body' not in data or 'id' not in data:
                return JsonResponse(status=400, data={"message": "Invalid data format"})

            user_id = data['id']
            user = get_object_or_404(User, pk=user_id)
            payload = {'head': data['head'], 'body': data['body']}
            send_user_notification(user=user, payload=payload, ttl=1000)

            return JsonResponse(status=200, data={"message": "Web push successful"})
        except TypeError:
            return JsonResponse(status=500, data={"message": "An error occurred"})


def activate_notification(request):
    print('Hey comment tu vas')
    profile = request.user.userprofile
    profile.notification = True
    profile.save()
    # if profile.notification == 'true':
    return HttpResponse(profile.notification)


'''
    if not profile.notification:
        profile.notification = 'True'
        profile.save()
        print(request.user.userprofile.notification)
        return HttpResponse("false")
    else:
        return HttpResponse("true")
'''


def list_activity_log(request):
    # PROBLEM WITH LINK
    data = request.user
    al = data.sportactivitynotifications.all()
    args = {'data': al}
    return render(request, 'accounts/activity_list.html', args)


def information(request, name):
    data = SportActivity.objects.get(activity_name=name)
    args = {'data': data}
    return render(request, 'accounts/information.html', args)


def todo(request):
    user = request.user
    todo_list = Todo.objects.filter(user=user).order_by('id')
    form = TodoForm()
    args = {'todo_list': todo_list, 'form': form}
    return render(request, 'accounts/todo.html', args)


@login_required
@require_POST
def addTodo(request):
    form = TodoForm(request.POST)
    print(request.POST['text'])
    if form.is_valid():
        user = request.user
        new_todo = Todo(text=request.POST['text'], user=user)
        new_todo.save()
    return redirect('todo')

def completeTodo(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    todo.complete = True
    todo.save()
    return redirect('todo')


def deleteCompleted(request):
    Todo.objects.filter(complete__exact=True).delete()
    return redirect('todo')

def deleteAdd(request):
    Todo.objects.all().delete()
    return redirect('todo')


