from django.db import models
from django.contrib.auth.models import User


class List(models.Model):
    ORDERED = 'ordered'
    UNORDERED = 'unordered'
    LIST_TYPE_CHOICES = [
        (ORDERED, 'Numbered (ordered)'),
        (UNORDERED, 'Bullets (unordered)'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')
    title = models.CharField(max_length=200)
    list_type = models.CharField(max_length=10, choices=LIST_TYPE_CHOICES, default=ORDERED)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_lists', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author.username}: {self.text[:40]}'


class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text
