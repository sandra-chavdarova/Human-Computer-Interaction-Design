from django.contrib import admin

from .models import *


# Register your models here.
class BandAdmin(admin.ModelAdmin):
    list_display = ("name", "country")


class BandEventInline(admin.StackedInline):
    model = BandEvent
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date")
    exclude = ("user",)
    inlines = [BandEventInline, ]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.user and BandEvent.objects.filter(event=obj).count() == 0:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if obj and request.user == obj.user and BandEvent.objects.filter(event=obj).count() == 0:
            return True
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(Band, BandAdmin)
admin.site.register(Event, EventAdmin)
