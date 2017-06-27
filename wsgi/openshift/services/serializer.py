from rest_framework import serializers
from .models import Message, Usage, FeatureUsage


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('author', 'text', 'timestamp',)


class UsageSerializer(serializers.HyperlinkedModelSerializer):
    # use everything, but the following are optional
    osReadable = serializers.CharField(required=False, allow_blank=True)
    application = serializers.CharField(required=False, allow_blank=True)
    component = serializers.CharField(required=False, allow_blank=True)
    ip = serializers.CharField(required=False, allow_blank=True)
    #uid = serializers.HyperlinkedIdentityField(view_name='UsageViewSet', format='html', lookup_field='Usage.uid')

    class Meta:
        model = Usage
        #fields = '__all__'
        fields = ['osReadable', 'application', 'component', 'url', 'uid', 'host',
                  'dateTime', 'osName', 'osArch', 'osVersion', 'ParaView',
                  'mantidVersion', 'mantidSha1', 'ip']


class FeatureSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FeatureUsage
        fields = ['url', 'type', 'name', 'internal', 'count', 'mantidVersion']

    def checkLength(self, value, length, label):
        if (len(value) != length):
            raise serializers.ValidationError(
                "value is not consistent with %s (length %d != %d)" % (label, len(value), length))

    def checkHex(self, value, label):
        for i in "0123456789abcdef":
            value = value.replace(i, "")

        if len(value) > 0:
            raise serializers.ValidationError(
                "'%s' is not consistent with %s" % (attrs[source], label))

    # def validate_uid(self, value):
    #   """uid should be an md5"""
    #   self.checkLength(value, 32, "md5")
    #   return value

    # def validate_host(self, value):
    #   """host should be an md5"""
    #   self.checkLength(value, 32, "md5")
    #   return value

    # def validate_mantidSha1(self, value):
    #   """mantidSha1 should be an sha1"""
    #   self.checkLength(value, 40, "sha1")
    #   self.checkHex(value, "sha1")
    #   return value
