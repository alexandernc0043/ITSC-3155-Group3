from base.models import Tutor, Course
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import render, redirect

def tutor_list(request):
    tutors = Tutor.objects.filter(verified=True)
    context = {
        'tutors': tutors
    }

    return render(request, 'base/tutor/tutor_list.html', context)



def update_course_tutor(request, pk, action):
    # filters courses to only get ones the user is in
    course = Course.objects.get(id=pk)
    session_data = request.session.get('referer', {}) # Gets referal page if exists
    
    if request.method == 'POST':
        try:
            tutor = Tutor.objects.get(user_account=request.user)
        except Tutor.DoesNotExist:
            tutor = Tutor.objects.create(user_account=request.user, verified=False)
        tutor.available = request.POST.get("time")
        tutor.save()
        if action == 'remove':
            course.tutor.remove(tutor)
            if not tutor.course.exists():
                tutor.verified = False
            tutor.save()
            messages.success(request, f'You have been deleted as tutor for {course.name} successfully!')
        if action == 'remove-application':
            course.pending_tutor.remove(tutor)
            messages.success(request, f'Course tutor application deleted successfully!')
        elif action == 'add':
            course.pending_tutor.add(tutor)
            messages.success(request, f'You have applied to tutor {course.name} successfully!')
        course.save()
        return redirect(session_data)
    
    # Add request referer to cookie so on post goes back to the referal page.
    request.session['referer'] = request.META.get('HTTP_REFERER')

    context = {
        'course': course,
        'remove': action == 'remove'
    }
    return render(request, 'base/tutor/add_remove_course_tutor.html', context)


def remove_tutor(request, pk):
    return update_course_tutor(request, pk, 'remove')

def remove_application(request, pk):
    return update_course_tutor(request, pk, 'remove-application')

def add_tutor(request, pk):
    return update_course_tutor(request, pk, 'add')

def tutor_applications(request):
    courses = Course.objects.annotate(num_pending_tutors=Count('pending_tutor')).filter(num_pending_tutors__gt=0)

    context = {
        'courses': courses
    }
    return render(request, 'base/tutor/tutor_applications.html', context)

def update_tutor(request, course_pk, tutor_pk, action):
    tutor = Tutor.objects.get(id=tutor_pk)
    session_data = request.session.get('referer', {}) # Gets referal page if exists
    
    if request.method == 'POST':
        course = Course.objects.get(id=course_pk)
        if action == 'accept':
            tutor.verified = True
            course.tutor.add(tutor)
            messages.success(request, f'{tutor} has been accepted as tutor for {course.name} successfully!')
        if action == 'deny':
            messages.success(request, f'{tutor} has been denied as tutor for {course.name} successfully!')
        course.pending_tutor.remove(tutor)
        course.save()
        if not tutor.course.exists():
            tutor.verified = False
        tutor.save()
        return redirect(session_data)
    
    # Add request referer to cookie so on post goes back to the referal page.
    request.session['referer'] = request.META.get('HTTP_REFERER')
    context = {
        'tutor': tutor,
        'accept': action == 'accept'
    }
    return render(request, 'base/tutor/accept_deny_tutor.html', context)