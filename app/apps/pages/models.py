# Create your models here.
from django.db import models


class Suscriptor(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Suscriptor"
        verbose_name_plural = "Suscriptores"
        ordering = ["-created_at"]


class Brand(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
    
    def format_dict(self):
        return {
            "src": self.logo.url,
            "alt": self.name,
        }


class SiteImages(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="site_images/")
    alt = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Imagen del sitio"
        verbose_name_plural = "Imagenes del sitio"


class Messages(models.Model):
    SERVICES = [
        ("marketing", "Marketing Digital"),
        ("web", "Desarrollo Web"),
        ("design", "Diseño Gráfico"),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    interest_service = models.CharField(max_length=100, choices=SERVICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
        ordering = ["-created_at"]
