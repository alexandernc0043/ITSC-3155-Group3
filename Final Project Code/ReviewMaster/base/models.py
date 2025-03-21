from django.db import models


# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=4)  # EX: ITSC, MATH, ITIS, etc

    def __str__(self):
        return self.name


class CourseNumber(models.Model):
    number = models.IntegerField()  # EX: 1110, 2214

    def __str__(self):
        return self.number


class Section(models.Model):
    section_number = models.CharField(max_length=3)  # EX: 001, 201, 100, etc

    def __str__(self):
        return self.section_number



class Course(models.Model):
    course_name = models.CharField(max_length=200)
    dept = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL) # NOT SURE IF SET NULL IS GOOD HERE
    number = models.ForeignKey(CourseNumber, null=True, on_delete=models.SET_NULL)
    section_number = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['dept','number']

    def __str__(self):
        return f'{self.course_name} -- {self.dept}-{self.number}-{self.section_number}'


class Professor(models.Model):
    name = models.CharField(max_length=100)
    rating = models.CharField(max_length=5)  # Will be Star Symbols / Emojis
    courses = models.ManyToManyField(Course, related_name='courses', blank=True)

    def __str__(self):
        return self.name

