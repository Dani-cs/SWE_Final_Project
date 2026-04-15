from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'followed')  # prevent duplicate follows

    def __str__(self):
        return f"{self.follower} follows {self.followed}"