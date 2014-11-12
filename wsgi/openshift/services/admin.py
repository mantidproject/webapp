from django.contrib import admin

# Register your models here.
from .models import Message

class MessageAdmin(admin.ModelAdmin):
   list_display = ('author','text', 'timestamp')

   admin.site.register(Message, MessageAdmin)
