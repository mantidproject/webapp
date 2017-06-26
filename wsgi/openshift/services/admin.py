from django.contrib import admin

# Register your models here.
from .models import Message, Usage, FeatureUsage, UsageLocation


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
                    'component')

class UsageLocationAdmin(admin.ModelAdmin):
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
admin.site.register(UsageLocation, UsageLocationAdmin)
admin.site.register(Usage, UsageAdmin)
admin.site.register(FeatureUsage, FeatureUsageAdmin)
