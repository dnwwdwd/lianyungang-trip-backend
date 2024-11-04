from django.db import models

class Evaluation(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
    reserveId = models.IntegerField()
    userId = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content
