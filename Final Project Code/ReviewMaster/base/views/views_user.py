from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
import re
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
            login(request, user)
            return redirect('home')
        else:
            # Error handling for registration
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            username = request.POST.get('username')
            pattern = r"^\w*(@|-|\.|\+|_)*\w*$"  # Regex to check that username only contains certain valid characters
            # Username validation
            if not re.match(pattern, username):
                messages.error(request, 'Username contains invalid characters')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')

            # Password validation
            if len(password1) < 8:
                messages.error(request, 'Password is too short')
            elif password1.isdigit():
                messages.error(request, 'Password must contain at least one letter')
            elif password1 != password2:
                messages.error(request, 'Passwords do not match')
            else:
                messages.error(request, 'An error has occurred during registration, please try again later')

    context = {
        'form': form,
        'page': page,
        'username': request.POST.get('username')  # Keeps username in form even if there's an error
    }
    return render(request, 'base/login_register.html', context=context)