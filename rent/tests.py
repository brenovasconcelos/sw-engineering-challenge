from rest_framework.test import APITestCase
from rest_framework import status
from rent.models import Rent
from locker.models import Locker
from bloq.models import Bloq
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone

class RentViewSetTestCase(APITestCase):

    def setUp(self):
        # Set up Locker instance (assuming the Locker model has an `is_occupied` and `status`)
        self.bloq = Bloq.objects.create(title="Test Title", address="Test Address")
        self.locker = Locker.objects.create(bloq_id=self.bloq, status="open", is_occupied=False)
        
        # URL for RentViewSet create action
        self.create_url = reverse('rent-list')
        
        # Rent status choices for validation tests
        self.valid_status = "waiting_dropoff"
        self.invalid_status = "invalid_status"

    def test_create_rent(self):
        """
        Test creating a Rent instance, ensuring the locker is marked as occupied
        and status is updated.
        """
        # Define data to create a rent instance
        rent_data = {
            'locker_id': self.locker.id,
            'weight': 10.5,
            'size': 'm'
        }

        # Send POST request to create the rent
        response = self.client.post(self.create_url, rent_data, format='json')

        # Assert that rent is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['locker_id'], self.locker.id)

        # Ensure that the locker status is updated to 'closed' and is occupied
        self.locker.refresh_from_db()
        self.assertTrue(self.locker.is_occupied)
        self.assertEqual(self.locker.status, 'closed')

    def test_create_rent_with_unavailable_locker(self):
        """
        Test creating a rent when the locker is unavailable (occupied or not open).
        """
        # Update the locker to be occupied
        self.locker.is_occupied = True
        self.locker.status = 'closed'
        self.locker.save()

        # Define data to create a rent instance
        rent_data = {
            'locker_id': self.locker.id,
            'weight': 10.5,
            'size': 'm'
        }

        # Send POST request to create the rent
        response = self.client.post(self.create_url, rent_data, format='json')

        # Assert that rent creation fails due to locker unavailability
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Locker is not available for rent.", response.data)

    def test_update_rent_status(self):
        """
        Test updating the status of a Rent instance.
        """
        # First, create a Rent instance
        rent = Rent.objects.create(
            locker_id=self.locker,
            weight=5.5,
            status=Rent.RentStatus.CREATED,
            size=Rent.RentSize.M,
        )

        # Define the URL for the update status action
        update_url = reverse('rent-update-status', kwargs={'pk': rent.id})

        # Define valid status to update
        update_data = {
            'status': self.valid_status
        }

        # Send PATCH request to update rent status
        response = self.client.patch(update_url, update_data, format='json')

        # Assert that rent status was updated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], self.valid_status)

    def test_update_rent_status_invalid(self):
        """
        Test that updating rent status to an invalid status returns an error.
        """
        # First, create a Rent instance
        rent = Rent.objects.create(
            locker_id=self.locker,
            weight=5.5,
            size=Rent.RentSize.M,
        )

        # Define the URL for the update status action
        update_url = reverse('rent-update-status', kwargs={'pk': rent.id})

        # Define invalid status
        update_data = {
            'status': self.invalid_status
        }

        # Send PATCH request to update rent status
        response = self.client.patch(update_url, update_data, format='json')

        # Assert that rent status update fails
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid status.", response.data['error'])

    def test_update_rent_status_without_status(self):
        """
        Test that trying to update rent status without providing the status field returns an error.
        """
        # First, create a Rent instance
        rent = Rent.objects.create(
            locker_id=self.locker,
            weight=5.5,
            size=Rent.RentSize.M,
        )

        # Define the URL for the update status action
        update_url = reverse('rent-update-status', kwargs={'pk': rent.id})

        # Send PATCH request without status data
        response = self.client.patch(update_url, {}, format='json')

        # Assert that rent status update fails due to missing status field
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid status", response.data['error'])
