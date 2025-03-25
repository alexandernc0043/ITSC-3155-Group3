from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=4)  # EX: ITSC, MATH, ITIS, etc

    def __str__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=100)
    rating = models.CharField(max_length=5)  # Will be Star Symbols / Emojis

    def __str__(self):
        return self.name


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_dept = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)  # NOT SURE IF SET NULL IS GOOD HERE
    course_number = models.IntegerField(null=False)
    course_students = models.ManyToManyField(User, related_name='students', blank=True)
    course_professors = models.ManyToManyField(Professor, related_name='professors', blank=True)

    class Meta:
        ordering = ['course_dept', 'course_number']

    def __str__(self):
        return f'{self.course_dept}-{self.course_number}'
