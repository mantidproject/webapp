from django.contrib import admin

# Register your models here.
from .models import Message, Usage

class MessageAdmin(admin.ModelAdmin):
   list_display = ('author','text', 'timestamp')

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

admin.site.register(Message, MessageAdmin)
admin.site.register(Usage, UsageAdmin)
