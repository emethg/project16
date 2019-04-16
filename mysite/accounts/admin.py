from django.contrib import admin
from .models import UserProfile, Product

# Register your models here.
admin.site.register(UserProfile)


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name_product', 'price', 'description')
    list_filter = ('name_product', 'price')

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


admin.site.register(Product, ProductAdmin)
