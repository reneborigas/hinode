# Generated by Django 2.1.1 on 2018-10-23 12:50

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20181019_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=tinymce.models.HTMLField(),
        ),
    ]
