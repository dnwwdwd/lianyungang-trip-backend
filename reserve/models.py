from django.db import models

class Reserve(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    scenicId = models.IntegerField()
    reserveTime = models.DateTimeField()
    lastReserveTime = models.DateTimeField()
    status = models.IntegerField(default=0)
    evaluationId = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id