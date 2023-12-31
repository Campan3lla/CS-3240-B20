# Generated by Django 4.1.7 on 2023-04-02 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling_app', '0010_studentschedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentschedule',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='studentschedule',
            name='submitted',
        ),
        migrations.AddField(
            model_name='studentschedule',
            name='status',
            field=models.CharField(choices=[('not_submitted', 'Not Submitted'), ('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='not_submitted', max_length=16),
            preserve_default=False,
        ),
    ]
