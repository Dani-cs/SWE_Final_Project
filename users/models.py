from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows_made')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} → {self.following.username}'


AVATAR_COLORS = [
    '#00b4d8',  # cyan
    '#3b82f6',  # blue
    '#8b5cf6',  # purple
    '#ef4444',  # red
    '#22c55e',  # green
    '#f97316',  # orange
    '#ec4899',  # pink
    '#eab308',  # gold
    '#14b8a6',  # teal
    '#94a3b8',  # slate
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_color = models.CharField(max_length=7, default='#00b4d8')

    def __str__(self):
        return f'{self.user.username} profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
