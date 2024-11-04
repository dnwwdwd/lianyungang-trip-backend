# Generated by Django 4.2.16 on 2024-11-04 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scenic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('imgs', models.CharField(max_length=1000)),
                ('tags', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('ticket', models.IntegerField()),
                ('star', models.IntegerField()),
                ('score', models.FloatField()),
                ('phone', models.CharField(max_length=100)),
                ('openTime', models.CharField(max_length=100)),
            ],
        ),
    ]
