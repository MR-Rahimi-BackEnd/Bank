from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction,StarUser
from django.db.models import F

@receiver(post_save , sender=Transaction)
def user_star(sender,instance,created,*args, **kwargs):
    if created and instance.amount>500:
        staruser , _ = StarUser.objects.get_or_create(user = instance.sender , defaults={'star':0})
        staruser.star +=1
        staruser.save()