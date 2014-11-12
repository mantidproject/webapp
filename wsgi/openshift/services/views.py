from django.shortcuts import render

# Create your views here.
from .models import Message
from rest_framework import viewsets
from .serializer import MessageSerializer

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Message.objects.all()
  serializer_class = MessageSerializer
