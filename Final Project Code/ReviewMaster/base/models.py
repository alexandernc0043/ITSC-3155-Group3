from django.db import models
from django.contrib.auth.models import User

# updates professor rating at given id. simple for now
def updateRatingAvg(professor_id):
    professor = Professor.objects.get(id=professor_id) # gets professor at database with given id
    
    reviews = Review.objects.filter(professor_id=professor_id) # reviews (query set) of professor

    sum = 0
    for review in reviews:
        sum += review.rating

    avg = sum / len(reviews)

    professor.rating = avg
    professor.save()

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
    name = models.CharField(max_length=200)  # Ex: Software Engineering
    department = models.ForeignKey(Department, null=True,  on_delete=models.SET_NULL)  # NOT SURE IF SET NULL IS GOOD HERE
    number = models.IntegerField(null=False)  # Ex: 3155
    students = models.ManyToManyField(User, related_name='students', blank=True)  # The students who are taking the course
    professor = models.ForeignKey(Professor, related_name='professor', on_delete=models.SET_NULL, null=True)  # The professor who teach the course
    section_number = models.IntegerField() # EX: 100
    credit_hours = models.IntegerField() # EX: 3

    class Meta:
        ordering = ['department', 'number', 'section_number']  # Order by department, number, and section number.

    def __str__(self):
        return f'{self.department}-{self.number}-{self.section_number}'  # Calling will return DEPT-####-###


class Review(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Review by {self.student.username} for {self.professor.name}'
