from django.db import models

class Scenic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    imgs = models.CharField(max_length=1000)
    tags = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    price = models.FloatField()
    ticket = models.IntegerField()
    star = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    phone = models.CharField(max_length=100)
    openTime = models.CharField(max_length=100)
    def __str__(self):
        return self.name