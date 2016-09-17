
from django.conf.urls import url, include
from django.contrib import admin


from models import User, Travel, Join

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

class TravelAdmin(admin.ModelAdmin):
    pass
admin.site.register(Travel, TravelAdmin)

class JoinAdmin(admin.ModelAdmin):
    pass
admin.site.register(Join, JoinAdmin)
