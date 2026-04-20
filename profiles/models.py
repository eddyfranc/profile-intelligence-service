import uuid6
from django.db import models


class Profile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid6.uuid7,
        editable=False
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )

    gender = models.CharField(max_length=10)
    gender_probability = models.FloatField()
    sample_size = models.IntegerField()

    age = models.IntegerField()
    age_group = models.CharField(max_length=20)

    country_id = models.CharField(max_length=10)
    country_probability = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "profiles"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["gender"]),
            models.Index(fields=["country_id"]),
            models.Index(fields=["age_group"]),
        ]

    def save(self, *args, **kwargs):
        # Normalize name to enforce idempotency
        if self.name:
            self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name