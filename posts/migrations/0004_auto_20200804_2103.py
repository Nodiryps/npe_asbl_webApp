# Generated by Django 3.0.3 on 2020-08-04 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_auto_20200802_2134'),
        ('posts', '0003_auto_20200803_1956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dogNamesList',
        ),
        migrations.AlterField(
            model_name='post',
            name='dog',
            field=models.ForeignKey(choices=[(None, None)], default='', on_delete=django.db.models.deletion.CASCADE, related_name='dogPost', to='dogs.Dog'),
        ),
    ]