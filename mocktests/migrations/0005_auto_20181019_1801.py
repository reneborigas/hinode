# Generated by Django 2.1.1 on 2018-10-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocktests', '0004_score_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='end_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='start_time',
            field=models.TimeField(null=True),
        ),
    ]
