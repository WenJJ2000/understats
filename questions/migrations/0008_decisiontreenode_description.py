# Generated by Django 4.2.4 on 2023-08-22 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_decisiontreenode_morethantwo_node_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='decisiontreenode',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
    ]
