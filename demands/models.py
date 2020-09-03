from django.db import models
from accounts.models import User
from dogs.models import Dog

class Demand(models.Model):
    objects = models.Manager()

    dog = models.ForeignKey(Dog, related_name='demandDog', on_delete=models.CASCADE, null=True, blank=True, default='')
    applicant = models.ForeignKey(User, related_name='demandApplicant', on_delete=models.CASCADE, null=True, blank=True, default='')
    demandDate = models.DateField(verbose_name='date de création', auto_now_add=True)
    # demandTypes -> 'adoption' or 'hosting'
    demandType = models.CharField(max_length=8)


    def __str__(self):
        return " | ".join([
            "Demand type: " + self.demandType,
            "Dog: " + self.dog.name,
            "Applicant: " + self.applicant.username,
            "Date: " + str(self.demandDate)
        ])
