# Generated by Django 4.1.5 on 2023-03-18 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling_app', '0008_alter_registrationinformation_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseidentifier',
            name='course_description',
            field=models.CharField(max_length=256),
        ),
    ]
