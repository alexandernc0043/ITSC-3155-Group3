from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.forms import UserForm, PasswordChange
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(username=pk)
    context = {
        'courses': user.students.all(),
        'user': user
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

        #Checks form validationm, updates user with new information 
        if userForm.has_changed() and userForm.is_valid() and passwordForm.has_changed() == False:
            userForm.save()
            return redirect('profile', pk=user.username)
        elif passwordForm.has_changed() and passwordForm.is_valid():
            passwordForm.save()
            update_session_auth_hash(request, passwordForm.user) #Prevents automatic user logout
            return redirect('profile', pk=user.username)
        else:
            return redirect('profile', pk=user.username)
        
    context = {
        'userForm': userForm,
        'passwordForm': passwordForm,
        'user': user,
        'courses': user.students.all(),
    }

    return render(request, 'base/editProfile.html', context)