# Generated by Django 5.1.6 on 2025-03-21 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_name_course_course_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['dept', '-number']},
        ),
        migrations.AlterField(
            model_name='coursenumber',
            name='number',
            field=models.IntegerField(max_length=4),
        ),
    ]
