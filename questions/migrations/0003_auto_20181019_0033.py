# Generated by Django 2.1.1 on 2018-10-18 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20181019_0033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentanswer',
            old_name='answer',
            new_name='choice',
        ),
    ]
