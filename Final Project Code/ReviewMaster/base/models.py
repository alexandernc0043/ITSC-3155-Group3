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
        else:
            return f'{self.user_account}'

class Professor(models.Model):
    name = models.CharField(max_length=100)  # First & Last Name (John Doe)
    avatar = models.ImageField(null=True, default='avatar.svg')
    verified = models.BooleanField(default=False)  # If the professor is verified by email
    user_account = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def rating(self):
        unflagged = self.review_set.filter(flagged=False)
        count = unflagged.count()
        if count == 0:
            return 'N/A'
        total = sum(review.rating for review in unflagged)
        average = round(total / count, 1)
        return f'{average} / 5'

    def rating_course(self, course):
        total = 0
        count = 0
        for review in self.review_set.all():
            if review.course == course:
                total += review.rating
                count += 1
        if total == 0:
            return 'N/A'
        return f'{int(round(total / count, 1))}'

    def __str__(self):
        if self.user_account and self.user_account.first_name and self.user_account.last_name:
            return f'{self.user_account.first_name} {self.user_account.last_name}'
        elif self.user_account and self.user_account.first_name:
            return f'{self.user_account.first_name}'
        else:
            return self.name

class Course(models.Model):
    name = models.CharField(max_length=200)  # Ex: Software Engineering
    # NOT SURE IF SET NULL IS GOOD HERE
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    # Ex: 3155
    number = models.IntegerField(null=False)
    # The students who are taking the course
    students = models.ManyToManyField(User, related_name='students', blank=True)
    # The professor who teach the course
    professor = models.ForeignKey(Professor, related_name='professor', on_delete=models.SET_NULL, default=None, null=True)
    section_number = models.IntegerField(null=True)
    tutor = models.ManyToManyField(Tutor, related_name='course', blank=True, null=True)
    pending_tutor = models.ManyToManyField(Tutor, related_name='courses', blank=True, null=True)
    # EX: 3
    credit_hours = models.IntegerField()

    class Meta:
        ordering = ['department', 'number']  # Order by department, number, and section number.
        unique_together = ('department', 'number', 'section_number')

    def __str__(self):
        return f'{self.department}-{self.number}'  # Calling will return DEPT-####

class Review(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    rating = models.IntegerField()
    course = models.ForeignKey(Course, related_name='course', on_delete=models.SET_NULL, null=True)
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Review by {self.student.username} for {self.professor.name}'
