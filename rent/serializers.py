from rest_framework import serializers
from .models import Rent

class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'
        read_only_fields = ['created_at']

    def save(self, **kwargs):
        # Get the Locker instance
        locker = self.validated_data['locker_id']

        # Update the Locker's state before saving Rent
        if not locker.is_occupied and locker.status == 'open':
            locker.is_occupied = True
            locker.status = 'closed'
            locker.save() 

            rent = super().save(**kwargs)
            return rent
        else:
            raise serializers.ValidationError("Locker is not available for rent.")
        