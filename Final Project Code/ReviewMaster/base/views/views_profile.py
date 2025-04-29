from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from base.forms import UserForm, PasswordChange
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from ..models import Professor, Tutor
from ..utils import check_username, check_password, handle_uploaded_file

def profile(request, pk):
    user = User.objects.get(username=pk)
    try:
        tutor = user.tutor
        courses_pending = tutor.courses.all()
        courses_tutor = tutor.course.all()
    except Tutor.DoesNotExist:
        tutor = None
        courses_pending = None
        courses_tutor = None

    context = {
        'courses': user.students.all(),
        'user': user,
        'reviews' : user.review_set.filter(flagged=False),
        'courses_pending': courses_pending,
        'courses_tutor': courses_tutor,
        'tutor': True if tutor else False
    }
    return render(request, 'base/profile/profile.html', context)

def save_image(request, professor):
    if professor and request.FILES.get('avatar'):
        file = request.FILES.get('avatar')
        file_path = handle_uploaded_file(file)
        professor.avatar = file_path
        professor.save()

@login_required(login_url='login')
def edit_profile(request, pk):
    user = User.objects.get(username=pk)
    userForm = UserForm(instance=user)
    passwordForm = PasswordChange(user)
    try:
        professor = Professor.objects.get(user_account=user)
    except Professor.DoesNotExist:
        professor = None
    option = request.POST.get('option') if request.POST.get('option') != None else 'no'

    if request.method == 'POST':
        userForm = UserForm(request.POST, instance=user)
        passwordForm = PasswordChange(user, request.POST)

        #Only changing username
        if option == "no" and userForm.is_valid():
            if professor and request.FILES.get('avatar'):
                save_image(request, professor)
            userForm.save()
            return redirect('profile', pk=user.username)
        #Changing both or just password
        if userForm.is_valid() and passwordForm.is_valid():
            if professor and request.FILES.get('avatar'):
                save_image(request, professor)
            userForm.save()
            passwordForm.save()
            update_session_auth_hash(request, passwordForm.user)
            return redirect('profile', pk=user.username)
        else:
            # Error handling for registration
            username = request.POST.get('username')
            # Username validation
            username_error_message = check_username(username, True)
            if username_error_message != '':
                messages.error(request, username_error_message)

            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')
            # Password validation
            password_error_message = check_password(password1, password2)
            if password_error_message != '':
                messages.error(request, password_error_message)
          
    context = {
        'userForm': userForm,
        'passwordForm': passwordForm,
        'user': user,
        'courses': user.students.all(),
        'reviews': user.review_set.all(),
        'option': option,
        'professor': professor,
        'avatar': professor.avatar.url if professor and professor.avatar else None
    }

    print("POST option:", request.POST.get('option'))
    return render(request, 'base/profile/edit_profile.html', context)

# @login_required(login_url='login')
# def editReview():
#     review = Review.objects.all()
