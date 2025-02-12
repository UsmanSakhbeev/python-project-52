# Generated by Django 5.1.4 on 2025-02-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0002_alter_task_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='labels', to='labels.label', verbose_name='Labels'),
        ),
    ]
