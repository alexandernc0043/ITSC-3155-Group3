from base.models import Professor, User, Course, Department
from django.shortcuts import redirect, render

def export_courses(request, pk):
    student = User.objects.get(username=pk)
    # course = []
    courses = student.students.all()
    # for i in Course.objects.all():
    #     course.append(i)

    context = {
        'student' : student,
        'courses': courses
    }

    return render(request, 'base/exportCourses.html', context)