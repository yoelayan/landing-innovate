from django.db import models


class Integration(models.Model):
    # Head, footer
    UBICATIONS = [
        ("head", "Head"),
        ("footer", "Footer"),
    ]
    name = models.CharField(max_length=255)
    code = models.TextField()
    ubication = models.CharField(max_length=255, choices=UBICATIONS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Integracion"
        verbose_name_plural = "Integraciones"
