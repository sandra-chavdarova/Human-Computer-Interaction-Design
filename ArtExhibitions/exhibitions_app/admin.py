from django.utils import timezone

from django.contrib import admin

from .models import *


# Register your models here.

class ArtistAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser


class ExhibitionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Exhibition.objects.filter(end_date__gt=timezone.now().date())
        elif Artist.objects.filter(user=request.user):
            return Exhibition.objects.filter(art__artist__user=request.user)
        return Exhibition.objects.all()


class ArtAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return Artist.objects.filter(user=request.user).exists()

    def save_model(self, request, obj, form, change):
        artist = Artist.objects.filter(user=request.user).first()
        obj.artist = artist
        return super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # дали логираниот корисник е тој уметник и
        # дали уметникот е истиот уметник со тој на делото
        return obj and Artist.objects.filter(user=request.user, id=obj.artist.id).exists()


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Art, ArtAdmin)
admin.site.register(Exhibition, ExhibitionAdmin)
