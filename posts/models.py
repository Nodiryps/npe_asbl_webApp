from django.db import models
from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter
from django.core import serializers
from accounts.models import User
from dogs.models import Dog


# class DogSerializer(BaseSerializer):
#     def serilize(self):
#         return repr(self.value), {'form dogs.models import Dog'}


class Post(models.Model):
    objects = models.Manager()


    def getAdoptedDogs():
        adoptedDogs = Dog.objects.filter(adopted=True)
        choices = []
        for dog in adoptedDogs:
            choices.append((dog, dog))
        # choices.sort()
        return tuple(choices)


    author = models.ForeignKey(
        User,
        related_name='userPost',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=''
    )
    dog = models.ForeignKey(
        Dog,
        related_name='dogPost',
        # choices=getAdoptedDogs(),
        on_delete=models.CASCADE,
        default=''
    )
    body = models.TextField(
        default='',
        max_length=500
    )
    postPicture = models.ImageField(
        default='defaultDog.png',
        blank=False
    )
    timestamp = models.DateTimeField(
        verbose_name='date de création',
        auto_now_add=True
    )


    def __str__(self):
        return '{}{}{}'.format(str(self.id),self.dog, self.author)