from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=4)  # EX: ITSC, MATH, ITIS, etc

    def __str__(self):
        return self.name  # Calling Department will return name
    
class Tutor(models.Model):
    avatar = models.ImageField(null=True, default='avatar.svg')
    verified = models.BooleanField(default=False)
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        if self.user_account and self.user_account.first_name and self.user_account.last_name:
            return f'{self.user_account.first_name} {self.user_account.last_name}'
        elif self.user_account and self.user_account.first_name:
            return f'{self.user_account.first_name}'
        elif self.user_account:
            return f'{self.user_account}'

class Professor(models.Model):
    name = models.CharField(max_length=100)  # First & Last Name (John Doe)
    avatar = models.ImageField(null=True, default='avatar.svg')
    verified = models.BooleanField(default=False)  # If the professor is verified by email
    user_account = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def rating(self):
        total = 0
        for review in self.review_set.all():
            total += review.rating
        if total == 0: # If no ratings we return 0
            return 'N/A'
        return f'{round(total / self.review_set.all().count(), 1)} / 5' # Rounds to tens place.
    
    def __str__(self):
        if self.user_account and self.user_account.first_name and self.user_account.last_name:
            return f'{self.user_account.first_name} {self.user_account.last_name}'
        elif self.user_account and self.user_account.first_name:
            return f'{self.user_account.first_name}'
        else: 
            return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)  # Ex: Software Engineering
    department = models.ForeignKey(Department, null=True,  on_delete=models.SET_NULL)  # NOT SURE IF SET NULL IS GOOD HERE
    number = models.IntegerField(null=False)  # Ex: 3155
    students = models.ManyToManyField(User, related_name='students', blank=True)  # The students who are taking the course
    professor = models.ManyToManyField(Professor, related_name='professor')  # The professor who teach the course
    tutor = models.ManyToManyField(Tutor, related_name='course', blank=True)
    credit_hours = models.IntegerField() # EX: 3

    class Meta:
        ordering = ['department', 'number']  # Order by department, number, and section number.

    def __str__(self):
        return f'{self.department}-{self.number}'  # Calling will return DEPT-####

class Review(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    course = models.ForeignKey(Course, related_name='course', on_delete=models.SET_NULL, null=True)
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Review by {self.student.username} for {self.professor.name}'