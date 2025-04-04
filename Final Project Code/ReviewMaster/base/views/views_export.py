from base.models import Professor, User, Course, Department
from django.shortcuts import redirect, render

def exportCourses(request, pk):
    student = User.objects.get(username=pk)
    courses = Course.objects.filter(students=student).get()

    context = {
        'student' : student,
        'courses' : courses
    }

    return render(request, 'base/exportCourses.html', context)