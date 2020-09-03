# Generated by Django 3.0.3 on 2020-08-02 19:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dogs', '0002_auto_20200802_2134'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(default='', max_length=500)),
                ('picture', models.ImageField(default='defaultDog.png', upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('author', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userPost', to=settings.AUTH_USER_MODEL)),
                ('dog', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dogPost', to='dogs.Dog')),
            ],
        ),
    ]
