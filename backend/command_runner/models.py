from django.db import models


class ManagementCommand(models.Model):
    """Used for registering the management commands page to admin (generates no db entries)"""

    class Meta:
        managed = False

    class ManagementCommandManager(models.Manager):
        def get_queryset(self):
            return None

    objects = ManagementCommandManager()
