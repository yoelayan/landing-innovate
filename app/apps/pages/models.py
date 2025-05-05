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
        return { "src": self.logo.url, "alt": self.name }

class SiteImages(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="site_images/")
    alt = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Imagen del sitio"
        verbose_name_plural = "Imágenes del sitio"

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

# Nuevo modelo Review
class Review(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="reviews")
    suscriptor = models.ForeignKey(Suscriptor, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)  # Puntuación de 1 a 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating} ⭐ de {self.suscriptor.email if self.suscriptor else 'Anónimo'}"

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
        ordering = ["-created_at"]
