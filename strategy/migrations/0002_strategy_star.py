# Generated by Django 4.2.16 on 2024-11-04 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='star',
            field=models.IntegerField(default=0),
        ),
    ]
