from django.contrib import admin
from .models import UserProfile, SportActivity

class SportActivityAdmin (admin.ModelAdmin):
    list_display = ('activity_name', 'description', 'time')
    list_filter = ('time', 'activity_name')

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete()

    def get_model_perms(self, request):
        """
        Return a dict of all perms for this model. This dict has the keys
        ``add``, ``change``, ``delete``, and ``view`` mapping to the True/False
        for each of those actions.
        """
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request),
        }


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(SportActivity, SportActivityAdmin)


