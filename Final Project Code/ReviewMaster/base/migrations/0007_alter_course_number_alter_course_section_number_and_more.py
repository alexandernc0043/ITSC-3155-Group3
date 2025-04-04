# Generated by Django 5.1.6 on 2025-03-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_coursenumber_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='number',
            field=models.IntegerField(default=111),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='section_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['dept', 'number']},
        ),
        migrations.DeleteModel(
            name='CourseNumber',
        ),
        migrations.DeleteModel(
            name='Section',
        ),
    ]
