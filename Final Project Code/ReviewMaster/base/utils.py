from django.contrib.auth.models import User
import re

def checkUsername(username, edit):
    message = ''
    pattern = r"^\w*(@|-|\.|\+|_)*\w*$"  # Regex to check that username only contains certain valid characters
    
    if not re.match(pattern, username):
        message = 'Username contains invalid characters'
    elif edit == False and User.objects.filter(username=username).exists():
        message = 'Username is already taken'

    return message

def checkPassword(password1, password2):
    message = ''
    if len(password1) < 8:
        message = 'Password is too short'
    elif password1.isdigit():
        message = 'Password must contain at least one letter'
    elif password1 != password2:
        message = 'Passwords do not match'
    else:
        message = 'The password is too common, try another one'

    return message