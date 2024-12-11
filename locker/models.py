from django.db import models
from bloq.models import Bloq


class Locker(models.Model):
    class LockerStatus(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'

    bloq_id = models.ForeignKey(Bloq, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=6,
        choices=LockerStatus.choices,
        default=LockerStatus.CLOSED,
    )
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Locker {self.id} at {self.bloq_id.address} is {self.status} and {'Occupied' if self.is_occupied else 'Available'}"
