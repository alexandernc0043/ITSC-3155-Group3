import os
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import re

def check_username(username, edit):
    message = ''
    pattern = r"^\w*(@|-|\.|\+|_)*\w*$"  # Regex to check that username only contains certain valid characters
    
    if not re.match(pattern, username):
        message = 'Username contains invalid characters'
    elif edit == False and User.objects.filter(username=username).exists():
        message = 'Username is already taken'

    return message

def check_password(password1, password2):
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

def handle_uploaded_file(file):
    upload_dir = 'uploads/'
    file_path = os.path.join(upload_dir, file.name)  

    # Ensure the upload directory exists
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Save the file to the media directory
    default_storage.save(file_path, ContentFile(file.read()))

    return file_path