from django.db import models
from django.contrib.auth.models import User




class Department(models.Model):
    name = models.CharField(max_length=4)  # EX: ITSC, MATH, ITIS, etc

    def __str__(self):
        return self.name  # Calling Department will return name


class Professor(models.Model):
    name = models.CharField(max_length=100)  # First & Last Name (John Doe)
    rating = models.CharField(max_length=3)  
    
    


   
    def __str__(self):
        return self.name  # Calling Professor will return name


class Course(models.Model):
    course_name = models.CharField(max_length=200)  # Ex: Software Engineering
    course_dept = models.ForeignKey(Department, null=True,
                                    on_delete=models.SET_NULL)  # NOT SURE IF SET NULL IS GOOD HERE
    course_number = models.IntegerField(null=False)  # Ex: 3155
    course_students = models.ManyToManyField(User, related_name='students',
                                             blank=True)  # The students who are taking the course
    course_professors = models.ManyToManyField(Professor, related_name='professors',
                                               blank=True)  # The professors who teach the course

    class Meta:
        ordering = ['course_dept', 'course_number']  # Order by department and number

    def __str__(self):
        return f'{self.course_dept}-{self.course_number}'  # Calling will return DEPT-####


class Review(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(null=True, blank=True)
    def __str__(self):
        return f'Review by {self.student.username} for {self.professor.name}'



