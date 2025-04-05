from base.models import Professor, User, Course, Department
from django.shortcuts import redirect, render

def exportCourses(request, pk):
    student = User.objects.get(username=pk)
    course = []
    course.append(Course.objects.values())

    context = {
        'student' : student,
        'courses': course
    }

    return render(request, 'base/exportCourses.html', context)