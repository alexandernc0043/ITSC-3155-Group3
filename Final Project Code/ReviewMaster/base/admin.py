from django.contrib import admin
from .models import Professor, Course, Department
# Register your models here.


admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Department)
