# Generated by Django 2.1.1 on 2018-10-23 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocktests', '0005_auto_20181019_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='result',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
