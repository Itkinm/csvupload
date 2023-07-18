from django.db import models

# Create your models here.
class GoogleUser(models.Model):
    tg_id = models.IntegerField(null=True)
    refresh_token = models.CharField(max_length=200, null=True)
    registered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tg_id)