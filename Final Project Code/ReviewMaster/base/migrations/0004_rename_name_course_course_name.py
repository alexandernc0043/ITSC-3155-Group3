# Generated by Django 5.1.6 on 2025-03-21 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_coursenumber_department_section_course_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='name',
            new_name='course_name',
        ),
    ]
