from django.contrib import admin
from django.db import models


class SingleObjectAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return True


class MoiSkladObjectMixin(models.Model):
    class Meta:
        abstract = True

    moisklad_id = models.CharField(max_length=255, null=True)
