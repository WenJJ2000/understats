# Generated by Django 4.2.4 on 2023-10-29 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_datafile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafile',
            name='description',
        ),
        migrations.AddField(
            model_name='datafile',
            name='confidence_level',
            field=models.DecimalField(decimal_places=3, default=0.95, max_digits=4),
        ),
    ]
