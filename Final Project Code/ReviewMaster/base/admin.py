from django.contrib import admin
from .models import Professor, Course, Department, Review, Tutor
# Register your models here.


admin.site.register(Professor)
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Review)
