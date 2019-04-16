from django.contrib import admin
from .models import UserProfile, SportActivity

class SportActivityAdmin (admin.ModelAdmin):
    list_display = ('activity_name', 'description', 'time')
    list_filter = ('time', 'activity_name')


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(SportActivity, SportActivityAdmin)


