from base.models import Tutor
from django.shortcuts import render

def tutor_list(request):
    tutors = Tutor.objects.filter(verified=True)
    context = {
        'tutors': tutors
    }

    return render(request, 'base/tutor/tutor_list.html', context)