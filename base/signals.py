from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from base.models import Profile


@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        group = Group.objects.get(name='regular_users')
        instance.groups.add(group)
        Profile.objects.create(user=instance)
        print('Profile Created!')

# post_save.connect(create_profile,sender=User)

@receiver(post_save,sender=User)
def update_profile(sender, instance, created,**kwargs):
    if created == False:
        instance.profile.save()
        print('Profle Updated!')
    

# post_save.connect(update_profile,sender=User)