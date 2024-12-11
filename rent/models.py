from django.db import models
from locker.models import Locker

class Rent(models.Model):

    class RentStatus(models.TextChoices):
        CREATED = ('created', 'Created')
        WAITING_DROPOFF = ('waiting_dropoff', 'Waiting Dropoff')
        WAITING_PICKUP = ('waiting_pickup', 'Waiting Pickup')
        DELIVERED = ('delivered', 'Delivered')

    class RentSize(models.TextChoices):
        XS = ('xs', 'XS')
        S = ('s', 'S')
        M = ('m', 'M')
        L = ('l', 'L')
        XL = ('xl', 'XL')

    locker_id = models.ForeignKey(Locker, on_delete=models.CASCADE)
    weight = models.FloatField()
    status = models.CharField(
        choices=RentStatus.choices,
        default=RentStatus.CREATED,
        max_length=15,
    )
    size = models.CharField(
        choices=RentSize.choices,
        max_length=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rent ID {self.id}, {self.status} on {self.locker_id}"

    def update_locker_status(self):
        # Define the status to locker behavior mapping using a dictionary
        status_mapping = {
            Rent.RentStatus.WAITING_DROPOFF: self._waiting_dropoff,
            Rent.RentStatus.WAITING_PICKUP: self._waiting_pickup,
            Rent.RentStatus.DELIVERED: self._delivered,
            Rent.RentStatus.CREATED: self._created,
        }

        # Get the corresponding behavior function based on Rent status
        update_function = status_mapping.get(self.status)

        if update_function:
            update_function()  # Call the corresponding function to update the locker status
        else:
            raise ValueError(f"Unknown RentStatus: {self.status}")

    def _waiting_dropoff(self):
        """Behavior for waiting_dropoff status"""
        self.locker_id.is_occupied = True
        self.locker_id.status = Locker.LockerStatus.OPEN  # Locker is now open for dropoff
        self.locker_id.save()

    def _waiting_pickup(self):
        """Behavior for waiting_pickup status"""
        self.locker_id.is_occupied = True
        self.locker_id.status = Locker.LockerStatus.CLOSED  # Locker is closed for pickup
        self.locker_id.save()

    def _delivered(self):
        """Behavior for delivered status"""
        self.locker_id.is_occupied = False
        self.locker_id.status = Locker.LockerStatus.OPEN  # Locker is now available after delivery
        self.locker_id.save()

    def _created(self):
        """Behavior for created status"""
        self.locker_id.is_occupied = False
        self.locker_id.status = Locker.LockerStatus.OPEN  # Locker is available when rent is created
        self.locker_id.save()
