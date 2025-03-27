from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from base.models import Department, Course


def home(request):
    return render(request, 'base/home.html')

def remove_course(request, pk):
    split = pk.split('-')
    dept = split[0]
    course_number = split[1]
    course = Course.objects.filter(department__name=dept, number=course_number).get()  # filters courses to only get ones the user is in
    context = {
        'remove': True,
        'course': course
    }
    if request.method == 'POST':
        course.students.remove(request.user)
        course.save()
        return redirect('courses')
    return render(request, 'base/addRemoveCourse.html', context)

def add_course(request, pk):
    dept = pk.split('-')[0] # gets department
    course_number = pk.split('-')[1] # gets course number
    course = Course.objects.filter(department__name=dept, number=course_number).get()
    if request.method == 'POST':
        course.students.add(request.user) # add student to course
        course.save() # save
        return redirect('courses') # redirect back to courses
    context = {
        'course': course,
        'pk': pk
    }
    return render(request, 'base/addRemoveCourse.html', context)


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


def register_user(request):
    page = 'register'
    form = UserCreationForm()
    context = {
        'form': form,
        'page': page
    }
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # form for registration
        if form.is_valid():
            user = form.save(commit=False) # Don't auto save form
            user.username = user.username.lower() # Make username lowercase
            # if form.password1 != form.password2:
            #     messages.error(request, 'Passwords do not match!')
            # else:
            user.save() # Saves user
            login(request, user) # Logs user in.
            return redirect('home') # redirect to home
        else:
            messages.error(request, 'An error has occurred during registration') # if form not valid return error
    return render(request, 'base/login_register.html', context=context)


@login_required(login_url='/login/')
def pick_courses(request):
    courses = Course.objects.all() # get all courses, will be filtered in the future
    context = {
        'departments': Department.objects.all(),
        'courses': courses,
    }
    return render(request, 'base/courses.html', context)

# def review(request, pk):
#    return render(request, 'base/review.html')
