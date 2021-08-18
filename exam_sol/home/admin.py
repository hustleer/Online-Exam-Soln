from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage, FAQ  , News  , Banner


class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title','company', 'update_at','status']

class BannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'update_at','link_type']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','ordernumber','status']
    list_filter = ['status']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['email']
    list_filter = ['email']




admin.site.register(Setting,SettingtAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Banner,BannerAdmin) 


