from base.models import Professor, User, Course, Department
from django.shortcuts import redirect, render

def exportCourses(request, pk):
    student = User.objects.get(username=pk)
    course = []
    for i in Course.objects.all():
        course.append(i)

    context = {
        'student' : student,
        'courses': course
    }

    return render(request, 'base/exportCourses.html', context)