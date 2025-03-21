from django.contrib import admin
from .models import Professor, Course, Section, CourseNumber, Department
# Register your models here.


admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Department)
admin.site.register(CourseNumber)