from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Rent
from .serializers import RentSerializer


class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer

    def create(self, request):
        """
        Handles the creation of a new Rent instance.

        This method processes HTTP POST requests, validates the provided data,
        and creates a new Rent instance in the database. If the data is invalid,
        it returns a 400 Bad Request response with error details.

        Args:
            request (Request): The HTTP request object containing the payload in request.data.

        Returns:
            Response: 
                - 201 Created: If the Rent instance is successfully created, returns the serialized data of the created instance.
                - 400 Bad Request: If the data validation fails, returns error details.
        """
        rent = RentSerializer(data=request.data)

        if not rent.is_valid():
            return Response(rent.errors, status=status.HTTP_400_BAD_REQUEST)
        
        rented = rent.save()

        return Response(self.get_serializer(rented).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        instance = self.get_object()

        new_status = request.data.get('status')

        if new_status not in [choice[0] for choice in Rent.RentStatus.choices]:
            return Response(
                {"error": f"Invalid status. Valid statuses are: {[choice[0] for choice in Rent.RentStatus.choices]}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance.status = new_status
        instance.update_locker_status()
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
