from django.utils import timezone
from django.contrib import admin
from .models import *


# Register your models here.

class AgentAdmin(admin.ModelAdmin):
    exclude = ("user",)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)


class AgentAdminInline(admin.StackedInline):
    model = AgentEstate
    extra = 0


class CharacteristicAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser


class CharacteristicAdminInline(admin.StackedInline):
    model = EstateCharacteristic
    extra = 0


class EstateAdmin(admin.ModelAdmin):
    inlines = [AgentAdminInline, CharacteristicAdminInline]

    def has_add_permission(self, request):
        return Agent.objects.filter(user=request.user).exists()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            agent = Agent.objects.filter(user=request.user).first()
            if agent:
                AgentEstate.objects.get_or_create(agent=agent, estate=obj)
                if obj.is_sold:  # if added already as sold, increment
                    agent.sales += 1
                    agent.save()

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return EstateCharacteristic.objects.filter(estate=obj).count() == 0

    def has_change_permission(self, request, obj=None):
        # ако се уште не менуваме ништо ќе помине овој if и ќе може да се види листата,
        # ако не помине тоа значи дека менуваме некој објект
        if obj is None:
            return Agent.objects.filter(user=request.user).exists()
        return AgentEstate.objects.filter(agent__user=request.user, estate=obj).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Estate.objects.filter(date=timezone.localdate())
        return Estate.objects.filter(agentestate__agent__user=request.user).distinct()


admin.site.register(Estate, EstateAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
