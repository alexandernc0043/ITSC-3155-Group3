from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from ..models import Professor
from ..utils import check_username, check_password

def logout_user(request):
    logout(request)
    return redirect('home')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)  # try and find that user object
        except:
            messages.error(request, 'Username or password incorrect')

        user = authenticate(request, username=username, password=password)  # authenticate the user

        if user is not None:
            login(request, user)  # Logins in user
            next_page = request.GET.get('next')  # if the url has a next Param
            if next_page:  # checks if next
                return redirect(next_page)  # redirects them to next page (used if login_required a thing)
            else:
                return redirect('home')  # else it brings them home
        else:
            messages.error(request, 'Username or password incorrect')
    return render(request, 'base/login_register.html')


def register_user(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # form for registration
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            professor = request.POST.get('professor')
            if professor:
                user_professor = Professor.objects.create(name=user.username, username=user, verified=False)
                user_professor.save()
            login(request, user)
            return redirect('home')
        else:
            # Error handling for registration
            username = request.POST.get('username')
            # Username validation
            username_error_message = check_username(username, False)
            if username_error_message != '':
                messages.error(request, username_error_message)

            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            # Password validation
            password_error_message = check_password(password1, password2)
            if password_error_message != '':
                messages.error(request, password_error_message)
            

    context = {
        'form': form,
        'page': page,
        'username': request.POST.get('username'),  # Keeps username in form even if there's an error
        'professor': request.POST.get('professor')
    }
    return render(request, 'base/login_register.html', context=context)