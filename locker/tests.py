from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from locker.models import Locker
from bloq.models import Bloq


class LockerViewSetTests(APITestCase):
    def setUp(self):
        # Create a sample Bloq instance
        self.bloq = Bloq.objects.create(address="123 Test Street")

        # Create sample Locker instances
        self.locker1 = Locker.objects.create(
            bloq_id=self.bloq,
            status=Locker.LockerStatus.CLOSED,
            is_occupied=False,
        )
        self.locker2 = Locker.objects.create(
            bloq_id=self.bloq,
            status=Locker.LockerStatus.OPEN,
            is_occupied=True,
        )

        # Initialize API Client
        self.client = APIClient()

        # Base URLs for testing
        self.locker_list_url = reverse('locker-list')
        self.locker_detail_url = lambda pk: reverse('locker-detail', args=[pk])

    def test_list_lockers(self):
        """Test retrieving a list of lockers."""
        response = self.client.get(self.locker_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two lockers created in setUp
        self.assertEqual(response.data[0]['id'], self.locker1.id)

    def test_retrieve_locker(self):
        """Test retrieving a single locker by ID."""
        response = self.client.get(self.locker_detail_url(self.locker1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.locker1.id)
        self.assertEqual(response.data['status'], self.locker1.status)

    def test_create_locker(self):
        """Test creating a new locker."""
        data = {
            "bloq_id": self.bloq.id,
            "status": Locker.LockerStatus.OPEN,
            "is_occupied": False,
        }
        response = self.client.post(self.locker_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Locker.objects.count(), 3)  # Two created in setUp + 1 new
        created_locker = Locker.objects.get(id=response.data['id'])
        self.assertEqual(created_locker.status, Locker.LockerStatus.OPEN)
        self.assertFalse(created_locker.is_occupied)

    def test_update_locker(self):
        """Test updating a locker's fields."""
        data = {
            "status": Locker.LockerStatus.OPEN,
            "is_occupied": True,
        }
        response = self.client.patch(self.locker_detail_url(self.locker1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.locker1.refresh_from_db()
        self.assertEqual(self.locker1.status, Locker.LockerStatus.OPEN)
        self.assertTrue(self.locker1.is_occupied)

    def test_delete_locker(self):
        """Test deleting a locker."""
        response = self.client.delete(self.locker_detail_url(self.locker1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Locker.objects.count(), 1)  # One locker remaining
        with self.assertRaises(Locker.DoesNotExist):
            Locker.objects.get(id=self.locker1.id)

    def test_invalid_create_locker(self):
        """Test creating a locker with invalid data."""
        data = {
            "status": "invalid_status",  # Invalid choice
            "is_occupied": True,
        }
        response = self.client.post(self.locker_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('bloq_id', response.data)
        self.assertIn('status', response.data)

    def test_retrieve_nonexistent_locker(self):
        """Test retrieving a locker that does not exist."""
        response = self.client.get(self.locker_detail_url(999))  # Nonexistent ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
