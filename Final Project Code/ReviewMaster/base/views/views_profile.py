from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.forms import UserForm, PasswordChange
from django.contrib.auth import update_session_auth_hash

from base.models import  Review

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(username=pk)
    context = {
        'courses': user.students.all(),
        'user': user,
        'reviews' : Review.objects.all()
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def edit_profile(request, pk):
    user = User.objects.get(username=pk)
    userForm = UserForm(instance=user)
    passwordForm = PasswordChange(user)

    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=user)
        passwordForm = PasswordChange(user, request.POST)

        #Only changing username
        if request.POST.get('option') == 'no' and userForm.is_valid():
            userForm.save()
            return redirect('profile', pk=user.username)
        #Changing both or just password
        if userForm.is_valid() and passwordForm.is_valid():
            userForm.save()
            passwordForm.save()
            update_session_auth_hash(request, passwordForm.user)
            return redirect('profile', pk=user.username)
          
    context = {
        'userForm': userForm,
        'passwordForm': passwordForm,
        'user': user,
        'courses': user.students.all(),
    }

    return render(request, 'base/editProfile.html', context)