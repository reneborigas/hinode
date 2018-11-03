# Generated by Django 2.1.1 on 2018-10-18 16:32

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.TextField(null=True)),
                ('overview', tinymce.models.HTMLField()),
                ('description', tinymce.models.HTMLField()),
                ('status', models.IntegerField(choices=[(1, 'ACTIVE'), (0, 'INACTIVE')], default=1)),
                ('deleted', models.BooleanField(blank=True, default=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('reviewprogram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.ReviewProgram')),
            ],
        ),
    ]
