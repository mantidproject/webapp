from django.contrib import admin

# Register your models here.
from .models import Message, Usage, FeatureUsage, Location


class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'timestamp')


class UsageAdmin(admin.ModelAdmin):
    list_display = ('uid',
                    'host',
                    'dateTime',
                    'osName',
                    'osArch',
                    'osReadable',
                    'osVersion',
                    'ParaView',
                    'mantidVersion',
                    'mantidSha1',
                    'application',
                    'component',
                    'ip')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('ip',
                    'city',
                    'region',
                    'country',
                    'latitude',
                    'longitude')

class FeatureUsageAdmin(admin.ModelAdmin):
    list_display = ('type',
                    'name',
                    'internal',
                    'count',
                    'mantidVersion')


admin.site.register(Message, MessageAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Usage, UsageAdmin)
admin.site.register(FeatureUsage, FeatureUsageAdmin)
