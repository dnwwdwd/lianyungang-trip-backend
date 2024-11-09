from django.db import models

class Strategy(models.Model):
    id = models.AutoField(primary_key=True)
    imgs = models.JSONField(max_length=1000)
    description = models.CharField(max_length=1000)
    content = models.CharField(max_length=10000)
    userId = models.IntegerField()
    type = models.IntegerField()
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    star = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name