from django.contrib import admin
from .models import *


# Register your models here.
class TripGuideInline(admin.TabularInline):
    model = TripGuide
    extra = 0


class GuideAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

class TripAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj:
            return TripGuide.objects.filter(trip=obj, guide__user=request.user).exists()

        return False

    def has_view_permission(self, request, obj=None):
        return True

admin.site.register(Trip)
admin.site.register(Guide, GuideAdmin)
