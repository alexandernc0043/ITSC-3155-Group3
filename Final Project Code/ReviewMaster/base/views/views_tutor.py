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

def update_tutor(request, pk, accept):
    tutor = Tutor.objects.get(id=pk)
    context = {
        'tutor': tutor,
        'accept': accept
    }
    return render(request, 'base/tutor/accept_deny_tutor.html', context)