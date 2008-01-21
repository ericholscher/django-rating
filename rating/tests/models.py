from django.db import models

class Movie(models.Model):
    name = models.CharField(maxlength=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
