# Generated by Django 5.1.6 on 2025-03-21 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_course_options_alter_coursenumber_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursenumber',
            name='number',
            field=models.IntegerField(),
        ),
    ]
