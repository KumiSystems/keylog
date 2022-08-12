from django.db import models
from django.contrib.auth import get_user_model


class Key(models.Model):
    application = models.CharField(max_length=256)
    key = models.CharField(max_length=256)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        get_user_model(), models.SET_NULL, null=True, related_name="keys_created")

    used_at = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(
        get_user_model(), models.SET_NULL, null=True, blank=True, related_name="keys_used")

    @property
    def used(self):
        return bool(self.used_at)