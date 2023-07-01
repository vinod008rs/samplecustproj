# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import CustomerModel
from .request_objects import CustomerProfileRequest
from .serializer import CustomerSerializer
from rest_framework.response import Response


class CustomerListCreateView(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomerModel.objects.filter(user=user)

    def perform_create(self, serializer):

        # Set the user ID on the serializer
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class CustomerRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomerModel.objects.filter(user=user)
