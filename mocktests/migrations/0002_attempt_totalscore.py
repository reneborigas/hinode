# Generated by Django 2.1.1 on 2018-10-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocktests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='totalscore',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]