from django.db import models

class StrategyStar(models.Model):
    id = models.AutoField(primary_key=True)
    strategyId = models.IntegerField()
    userId = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)
