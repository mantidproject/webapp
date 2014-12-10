from django.shortcuts import render

# Create your views here.
from .models import Message, Usage
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from .serializer import MessageSerializer, UsageSerializer

class MessageViewSet(viewsets.ModelViewSet):
  queryset = Message.objects.all()
  serializer_class = MessageSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]

class UsageViewSet(viewsets.ModelViewSet):
  queryset = Usage.objects.all()
  serializer_class = UsageSerializer
  permission_classes = [AllowAny]