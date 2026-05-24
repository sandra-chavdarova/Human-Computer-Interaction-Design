from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Estate, AgentEstate, Agent

@receiver(pre_save, sender=Estate)
def increment_agent_sales(sender, instance, **kwargs):
    if instance.pk: # existing estate being updated
        old = Estate.objects.get(pk=instance.pk)
        if not old.is_sold and instance.is_sold:  # flipped to sold
            agents = Agent.objects.filter(agentestate__estate=instance)
            agents.update(sales=models.F('sales') + 1)
