from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
import re
from .forms import UserForm, PasswordChange
from django.contrib.auth import update_session_auth_hash

from base.models import Department, Course



def home(request):
    return render(request, 'base/home.html')


@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(username=pk)
    context = {
        'courses': user.students.all(),
        'user': user
    }
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def editProfile(request, pk):
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

def addCourse(request, pk):
    dept = pk.split('-')[0] # gets department
    courseNumber = pk.split('-')[1] # gets course number
    course = Course.objects.filter(course_dept__name__icontains=dept, course_number=courseNumber).get() # filters courses

def removeCourse(request, pk):
    dept = pk.split('-')[0]  # gets department
    courseNumber = pk.split('-')[1]  # gets course number
    course = Course.objects.filter(course_dept__name__icontains=dept,
                                   course_number=courseNumber).get()  # filters courses
    context = {
        'remove': True,
        'course': course
    }
    if request.method == 'POST':
        course.course_students.remove(request.user)
        course.save()
        # Redirect to previous url not working with usual HTTP_REFERER, probably manually store path for redirection
        return redirect('courses')
    return render(request, 'base/addRemoveCourse.html', context)


def addCourse(request, pk):
    dept = pk.split('-')[0]  # gets department
    courseNumber = pk.split('-')[1]  # gets course number
    course = Course.objects.filter(course_dept__name__icontains=dept,
                                   course_number=courseNumber).get()  # filters courses
    if request.method == 'POST':
        course.course_students.add(request.user)  # add student to course
        course.save()  # save
        return redirect('courses')  # redirect back to courses
    context = {
        'course': course,
        'pk': pk
    }
    return render(request, 'base/addRemoveCourse.html', context)


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
        form = UserCreationForm(request.POST)  # form for registration
        if form.is_valid():
            user = form.save(commit=False)  # Don't auto save form
            user.username = user.username.lower()  # Make username lowercase
            # if form.password1 != form.password2:
            #     messages.error(request, 'Passwords do not match!')
            # else:
            user.save()  # Saves user
            login(request, user)  # Logs user in.
            return redirect('home')  # redirect to home
        else:
            messages.error(request, 'An error has occurred during registration')  # if form not valid return error
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
        'professors': professors,
        'reviews': Review.objects.filter()
    }

    return render(request, 'base/professor_list.html', context)


def professor_reviews(request, professor_name):
    professors = Professor.objects.filter(name=professor_name)
    professor = professors.first()
    reviews = Review.objects.filter(professor=professor)

    return render(request, 'base/professor_reviews.html', {'professor': professor, 'reviews': reviews})
