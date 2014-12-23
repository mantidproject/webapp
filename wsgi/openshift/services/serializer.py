from rest_framework import serializers
from .models import Message, Usage

class MessageSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Message
    fields = ('author','text','timestamp',)

class UsageSerializer(serializers.ModelSerializer):
  # use everything, but the following are optional
  osReadable = serializers.CharField(required=False)
  application = serializers.CharField(required=False)
  component = serializers.CharField(required=False)

  class Meta:
    model = Usage

  def checkLength(self, attrs, source, length, label):
    value = attrs[source]
    if (len(value) != length):
      raise serializers.ValidationError("value is not consistent with %s (length %d != %d)" % (label, len(value), length))
    return attrs

  def checkHex(self, attrs, source, label):
    value = attrs[source]
    for i in "0123456789abcdef":
      value = value.replace(i, "")

    if len(value) > 0:
      raise serializers.ValidationError("'%s' is not consistent with %s" % (attrs[source], label))
    return attrs

  def validate_uid(self, attrs, source):
    """uid should be an md5"""
    attrs = self.checkLength(attrs, source, 32, "md5")
    return attrs

  def validate_host(self, attrs, source):
    """host should be an md5"""
    attrs = self.checkLength(attrs, source, 32, "md5")
    return attrs

  def validate_mantidSha1(self, attrs, source):
    """mantidSha1 should be an sha1"""
    attrs = self.checkLength(attrs, source, 40, "sha1")
    attrs = self.checkHex(attrs, source, "sha1")
    return attrs
