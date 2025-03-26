from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

from base.models import Department, Course, Professor, Review


def home(request):
    return render(request, 'base/home.html')


def addCourse(request, pk):
    dept = pk.split('-')[0]  # gets department
    courseNumber = pk.split('-')[1]  # gets course number
    course = Course.objects.filter(course_dept__name__icontains=dept, course_number=courseNumber).get()  # filters courses
    if request.method == 'POST':
        course.course_students.add(request.user)  # add student to course
        course.save()  # save
        return redirect('courses')  # redirect back to courses
    context = {
        'course': course,
        'pk': pk
    }
    return render(request, 'base/addCourse.html', context)


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


@login_required(login_url='/login/')
def pick_courses(request):
    # Prefetch related professors for each course to optimize database queries
    courses = Course.objects.prefetch_related('course_professors').all()

    context = {
        'departments': Department.objects.all(),
        'courses': courses,
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
        
        return HttpResponse("Review submitted successfully!")
    else:
        return HttpResponse("Invalid request method", status=400)
    


def professor_list(request):
        professors = Professor.objects.all()

        context = {
        'professors': professors
    }
    
        
        return render(request, 'base/professor_list.html', context )


from django.shortcuts import render
from django.http import Http404
from .models import Professor, Review

def professor_reviews(request, professor_name):
    
    professors = Professor.objects.filter(name=professor_name)
    
   
    
    
    professor = professors.first()
    
    
    reviews = Review.objects.filter(professor=professor)

    return render(request, 'base/professor_reviews.html', {'professor': professor, 'reviews': reviews})

