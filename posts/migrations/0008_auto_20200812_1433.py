# Generated by Django 3.0.3 on 2020-08-12 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_auto_20200802_2134'),
        ('posts', '0007_auto_20200811_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='dog',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='dogPost', to='dogs.Dog'),
        ),
    ]
