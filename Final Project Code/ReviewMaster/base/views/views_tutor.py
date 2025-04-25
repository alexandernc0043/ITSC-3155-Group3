from base.models import Tutor, Course
from django.shortcuts import render

def tutor_list(request):
    tutors = Tutor.objects.filter(verified=True)
    context = {
        'tutors': tutors
    }

    return render(request, 'base/tutor/tutor_list.html', context)

def tutor_applications(request):
    tutors = Tutor.objects.filter(verified=False)
    context = {
        'tutors': tutors
    }
    return render(request, 'base/tutor/tutor_applications.html', context)

def update_tutor(request, pk):
    tutor = Tutor.objects.get(id=pk)
    context = {
        'tutor': tutor
    }

    return render(request, 'base/tutor/add_remove_course_tutor.html', context)