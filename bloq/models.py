from django.db import models


class Bloq(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.address}"
