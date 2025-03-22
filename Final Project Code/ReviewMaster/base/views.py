from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from base.models import Department, Course


def home(request):
    return render(request, 'base/home.html')


def logoutuser(request):
    logout(request)
    return redirect('home')


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)  # try and find that user object
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)  # authenticate the user

        if user is not None:
            login(request, user)  # Logins in user
            next_page = request.GET.get('next')  # if the url has a next Param
            if next_page:  # checks if next
                return redirect(next_page)  # redirects them to next page (used if login_required a thing)
            else:
                return redirect('home')  # else it brings them home
        else:
            messages.error(request, 'Username or password does not exist')
    return render(request, 'base/login_register.html')


def registeruser(request):
    page = 'register'
    form = UserCreationForm()
    context = {
        'form': form,
        'page': page
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')
    return render(request, 'base/login_register.html', context=context)


@login_required(login_url='/login/')
def pick_courses(request):
    query = request.GET.get('q')
    department = ''
    course_number = ''

    if '-' in query:
        split = query.split('-')
        department = split[0]
        course_number = split[1]
    if department and course_number:
        courses = Course.objects.filter(dept__name__icontains=department, number__number__icontains=course_number)
    elif department:
        courses = Course.objects.filter(dept__name__icontains=department)
    else:
        courses = Course.objects.all()

    context = {
        'departments': Department.objects.all(),
        'courses': courses,
        'query': query,
        'department': department,
        'course_number': course_number
    }
    return render(request, 'base/courses.html', context)

# def review(request, pk):
#    return render(request, 'base/review.html')
