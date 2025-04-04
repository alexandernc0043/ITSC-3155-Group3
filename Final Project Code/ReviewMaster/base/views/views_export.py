from base.models import Professor, User, Course, Department
from django.shortcuts import redirect, render

def exportCourses(request, pk):
    student = User.objects.get(username=pk)
    

    context = {
        'student' : student,
        'courses': student.students.all()
    }

    return render(request, 'base/exportCourses.html', context)