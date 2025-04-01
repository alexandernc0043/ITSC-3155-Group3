from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.forms import UserForm, PasswordChange
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from ..utils import checkUsername, checkPassword

from base.models import Review

@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(username=pk)
    context = {
        'courses': user.students.all(),
        'user': user,
        'reviews' : user.review_set.all()
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def edit_profile(request, pk):
    user = User.objects.get(username=pk)
    userForm = UserForm(instance=user)
    passwordForm = PasswordChange(user)
    option = request.POST.get('option') if request.POST.get('option') != None else 'no'

    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=user)
        passwordForm = PasswordChange(user, request.POST)

        #Only changing username
        if option == 'no' and userForm.is_valid():
            userForm.save()
            return redirect('profile', pk=user.username)
        #Changing both or just password
        if userForm.is_valid() and passwordForm.is_valid():
            userForm.save()
            passwordForm.save()
            update_session_auth_hash(request, passwordForm.user)
            return redirect('profile', pk=user.username)
        else:
            # Error handling for registration
            username = request.POST.get('username')
            # Username validation
            username_error_message = checkUsername(username, True)
            if username_error_message != '':
                messages.error(request, username_error_message)

            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')
            # Password validation
            password_error_message = checkPassword(password1, password2)
            if password_error_message != '':
                messages.error(request, password_error_message)
          
    context = {
        'userForm': userForm,
        'passwordForm': passwordForm,
        'user': user,
        'courses': user.students.all(),
        'reviews': user.review_set.all(),
        'option': option
    }

    return render(request, 'base/editProfile.html', context)

# @login_required(login_url='login')
# def editReview():
#     review = Review.objects.all()
