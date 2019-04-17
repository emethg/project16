from django.contrib import admin
from .models import UserProfile
from .models import Dish
from .models import Tip

# Register your models here.
admin.site.register(UserProfile)


class DishAdmin(admin.ModelAdmin):

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        return form.save(commit=False)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        formset.save()


admin.site.register(Dish, DishAdmin)


class TipAdmin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        obj.delete()

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        return form.save(commit=False)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        formset.save()


admin.site.register(Tip, TipAdmin)







