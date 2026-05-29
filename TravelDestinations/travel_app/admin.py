from django.contrib import admin
import random
from django.contrib import messages

from .models import *


# Register your models here.

class TravelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        guide = Guide.objects.filter(user=request.user).first()
        destinations = Travel.objects.filter(guide=guide)
        return request.user.is_superuser and destinations.count() < 5

    def save_model(self, request, obj, form, change):
        guide = Guide.objects.filter(user=request.user).first()
        destinations = Travel.objects.filter(guide=guide)
        total = 0.0
        for x in destinations.values_list("price", flat=True):
            total += float(x)
        if change:
            old_obj = Travel.objects.filter(pk=obj.pk).first()
            total -= old_obj.price

        total += obj.price
        if total < 50000:
            return super().save_model(request, obj, form, change)
        return self.message_user(request, "Total price exceeds 50 000!", level=messages.ERROR)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        guide = Guide.objects.filter(user=request.user).first()
        return obj.guide == guide


class GuideAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return obj and request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return obj and request.user.is_superuser

    def delete_model(self, request, obj):
        destinations = Travel.objects.filter(guide=obj)
        other_guides = Guide.objects.exclude(pk=obj.pk)
        available_guides = [g for g in other_guides if Travel.objects.filter(guide=g).count() < 5]

        for destination in destinations:
            random_guide = random.choice(list(available_guides))
            destination.guide = random_guide
            destination.save()
        super().delete_model(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            travels = [g.id for g in qs if Travel.objects.filter(guide=g).count() < 3]
            return qs.filter(id__in=travels)
        return qs


admin.site.register(Travel, TravelAdmin)
admin.site.register(Guide, GuideAdmin)
