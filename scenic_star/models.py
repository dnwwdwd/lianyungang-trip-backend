from django.db import models

class ScenicStar(models.Model):
    id = models.AutoField(primary_key=True)
    scenicId = models.IntegerField()
    userId = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id