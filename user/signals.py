from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for user: {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    print(f"Profile saved for user: {instance.username}")

@receiver(post_save, sender=Reserve_slot)
def create_or_update_fixture(sender, instance, created, **kwargs):
    if created:  # Only handle creation events
        conflicting_slots = Reserve_slot.objects.filter(slot=instance.slot).exclude(id=instance.id)
        for conflicting_slot in conflicting_slots:
            # Check if a fixture already exists for this conflicting pair
            existing_fixture = Fixture.objects.filter(
                (models.Q(team_1=instance.team, team_2=conflicting_slot.team) | 
                 models.Q(team_1=conflicting_slot.team, team_2=instance.team)),
                slot=instance.slot
            ).exists()
            if not existing_fixture:
                Fixture.objects.create(
                    team_1=instance.team,
                    team_2=conflicting_slot.team,
                    slot=instance.slot
                )
                print(f"Created Fixture for {instance.team} vs {conflicting_slot.team} at {instance.slot}")
            


# @receiver(post_save, sender=Reserve_slot)
# def delete_fixture(sender, instance, **kwargs):
#     conflicting_slot = Reserve_slot.objects.filter(slot=instance.slot).exclude(team=instance.team).first()
#     if conflicting_slot:
#         fixture = Fixture.objects.filter(team_1=instance.team, team_2=conflicting_slot.team, slot=instance.slot).first()
#         if fixture:
#             fixture.delete()
#             print(f"Deleted Fixture for {instance.team} vs {conflicting_slot.team} at {instance.slot}")

#             # Check if there are any remaining Reserve_slots for this slot
#             remaining_reserve_slots = Reserve_slot.objects.filter(slot=instance.slot).exists()
#             if not remaining_reserve_slots:
#                 # Update the slot availability to True if no remaining reserve slots
#                 instance.slot.available = True
#                 instance.slot.save()
#                 print(f"Updated Slot {instance.slot} availability to True")

