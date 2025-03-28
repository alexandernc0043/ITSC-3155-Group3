from base.models import Department, Course, Professor, Review
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
import re


def home(request):
    return render(request, 'base/home.html')


def update_course(request, pk, action):
    split = pk.split('-')
    dept = split[0]
    course_number = split[1]
    course = Course.objects.filter(department__name=dept,
                                   number=course_number).get()  # filters courses to only get ones the user is in
    if request.method == 'POST':
        if action == 'remove':
            course.students.remove(request.user)
            messages.success(request, 'Course removed successfully!')
        elif action == 'add':
            course.students.add(request.user)
            messages.success(request, 'Course added successfully!')
        course.save()
        return redirect('courses')

    context = {
        'course': course,
        'remove': action == 'remove'
    }
    return render(request, 'base/addRemoveCourse.html', context)


def remove_course(request, pk):
    return update_course(request, pk, 'remove')


def add_course(request, pk):
    return update_course(request, pk, 'add')


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

def pick_courses(request):
    # # Prefetch related professors for each course to optimize database queries
    # courses = Course.objects.prefetch_related('course_professors').all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q != '':
        courses = Course.objects.filter(
            Q(name__icontains=q) |
            Q(department__name__icontains=q) |
            Q(number__icontains=q) |
            Q(professor__name__icontains=q)
        )
    else:
        courses = Course.objects.all()  # get all courses, will be filtered in the future
        
    context = {
        'departments': Department.objects.all(),
        'courses': courses,
        'q': q
    }

    return render(request, 'base/courses.html', context)


@login_required
def review(request):
    professors = Professor.objects.all()

    context = {
        'professors': professors
    }
    return render(request, 'base/review.html', context)


@login_required
def submit_review(request):
    if request.method == 'POST':
        user = request.user

        professor_id = request.POST.get("professor")
        professor = Professor.objects.get(id=professor_id)

        rating = request.POST.get("rating")

        review = request.POST.get("review")

        review = Review(professor=professor, student=user, rating=rating, review=review)
        review.save()
        messages.success(request, 'Review successfully submitted!')

    else:
        messages.error(request, 'An error has occurred, please try again!')
    return redirect('review')



def professor_list(request):
    professors = Professor.objects.all()
    context = {
        'professors': professors
    }

    return render(request, 'base/professor_list.html', context)


def professor_reviews(request, professor_name):
    professors = Professor.objects.filter(name=professor_name)
    professor = professors.first()
    reviews = Review.objects.filter(professor=professor)

    return render(request, 'base/professor_reviews.html', {'professor': professor, 'reviews': reviews})
