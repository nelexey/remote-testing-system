from django.db import models
from django.conf import settings

class Test(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tests'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    test_data = models.JSONField()  # JSON для хранения вопросов и ответов
    difficulty = models.CharField(
        max_length=10,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium'
    )
    attempts_allowed = models.PositiveIntegerField(default=1)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Statistics(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='statistics'
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='statistics'
    )
    result = models.IntegerField()
    max_result = models.IntegerField()
    time_spent = models.DurationField()
    date_taken = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"
