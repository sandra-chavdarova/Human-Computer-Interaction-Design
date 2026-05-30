from django.contrib import admin
from .models import *
import random
from django.contrib import messages


# Register your models here.

class BakerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def delete_model(self, request, obj):
        cakes = Cake.objects.filter(baker=obj)
        other_bakers = Baker.objects.exclude(pk=obj.pk)
        for cake in cakes:
            baker = random.choice(list(other_bakers))
            cakes_baker = Cake.objects.filter(baker=baker)
            total = 0.0
            for c in cakes_baker:
                total += c.price
            if Cake.objects.filter(baker=baker).count() < 10 and total + cake.price < 10000:
                cake.baker = baker
                cake.save()
        return super().delete_model(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            bakers = [b.id for b in qs if Cake.objects.filter(baker=b).count() < 5]
            return qs.filter(id__in=bakers)
        return qs


class CakeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        baker = Baker.objects.filter(user=request.user).first()
        if baker:
            cakes = Cake.objects.filter(baker=baker).count()
            return cakes < 10
        return False

    def save_model(self, request, obj, form, change):
        baker = Baker.objects.filter(user=request.user).first()
        cakes = Cake.objects.filter(baker=baker)
        total = 0.0
        for cake in cakes:
            total += cake.price
        if change:
            total -= obj.price
        if total + obj.price < 10000:
            return super().save_model(request, obj, form, change)
        return self.message_user(request, "Total price of cakes cannot exceed 10000.", level=messages.ERROR)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        baker = Baker.objects.filter(user=request.user).first()
        return obj.baker == baker


admin.site.register(Cake, CakeAdmin)
admin.site.register(Baker, BakerAdmin)
