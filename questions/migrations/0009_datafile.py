# Generated by Django 4.2.4 on 2023-10-23 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_decisiontreenode_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datafile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]