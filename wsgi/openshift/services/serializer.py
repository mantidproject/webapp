from rest_framework import serializers
from .models import Message, Usage

class MessageSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Message
    fields = ('author','text','timestamp',)

class UsageSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Usage
    fields = ('uid',
              'host',
              'dateTime',
              'osName',
              'osArch',
              'osVersion',
              'ParaView',
              'mantidVersion',
              'mantidSha1')
