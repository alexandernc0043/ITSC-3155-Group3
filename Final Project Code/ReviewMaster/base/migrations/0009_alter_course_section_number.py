# Generated by Django 5.1.6 on 2025-03-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_course_number_alter_course_section_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='section_number',
            field=models.IntegerField(null=True),
        ),
    ]
