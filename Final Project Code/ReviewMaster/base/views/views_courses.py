from base.models import Department, Course, Tutor
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect

def update_course(request, pk, action):
    # filters courses to only get ones the user is in
    course = Course.objects.get(id=pk)
    session_data = request.session.get('referer', {}) # Gets referal page if exists
    
    if request.method == 'POST':
        if action == 'remove':
            course.students.remove(request.user)
            messages.success(request, 'Course removed successfully!')
        elif action == 'add':
            course.students.add(request.user)
            messages.success(request, 'Course added successfully!')
        course.save()
        return redirect(session_data)
    
    # Add request referer to cookie so on post goes back to the referal page.
    request.session['referer'] = request.META.get('HTTP_REFERER')

    context = {
        'course': course,
        'remove': action == 'remove'
    }
    return render(request, 'base/course/add_remove_course.html', context)


def remove_course(request, pk):
    return update_course(request, pk, 'remove')


def add_course(request, pk):
    return update_course(request, pk, 'add')

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
        courses = Course.objects.all()

    try:
        tutor = Tutor.objects.filter(user_account=request.user).first()
    except:
        tutor = None

    context = {
        'departments': Department.objects.all(),
        'courses': courses,
        'tutor': tutor,
        'q': q,
        'actions': True
    }

    return render(request, 'base/course/courses.html', context)

def course_page(request,pk):
    # courses = Course
    return None