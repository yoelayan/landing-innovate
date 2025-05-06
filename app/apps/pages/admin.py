from django.contrib import admin
from django.utils.html import format_html
from .models import Brand, Suscriptor, SiteImages, Messages, Review, FAQ

class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "image_thumbnail")
    list_editable = ("order",)
    search_fields = ("name",)
    ordering = ("order",)

    def image_thumbnail(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.logo.url)
        return "No Image"

    image_thumbnail.short_description = "Thumbnail"

class SuscriptorAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at")
    search_fields = ("email",)
    readonly_fields = ("created_at",)
    list_filter = ("created_at",)

class SiteImagesAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "image_thumbnail")
    search_fields = ("name", "code")
    list_filter = ("name",)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"

    image_thumbnail.short_description = "Thumbnail"

class MessagesAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "interest_service", "created_at")
    search_fields = ("name", "email", "message")
    list_filter = ("interest_service", "created_at")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Contact Information", {"fields": ("name", "email")}),
        ("Message Details", {"fields": ("message", "interest_service", "created_at")}),
    )

# Configuración para administrar Reviews
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "created_at")
    search_fields = ("name", "comment")
    list_filter = ("rating", "created_at")
    readonly_fields = ("created_at",)
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"

    image_thumbnail.short_description = "Thumbnail"

# Configuración para administrar FAQ
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "created_at")
    search_fields = ("question", "answer")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

    

admin.site.register(Brand, BrandAdmin)
admin.site.register(Suscriptor, SuscriptorAdmin)
admin.site.register(SiteImages, SiteImagesAdmin)
admin.site.register(Messages, MessagesAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FAQ, FAQAdmin)