# Generated by Django 2.2.6 on 2019-11-06 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_to',
        ),
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(blank=True, related_name='developer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='task', to=settings.AUTH_USER_MODEL),
        ),
    ]
