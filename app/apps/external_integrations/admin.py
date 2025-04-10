from django.contrib import admin
from .models import Integration


# Integracion con admin
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("name", "ubication", "code_preview")
    search_fields = ("name", "ubication", "code")
    list_filter = ("ubication",)
    fieldsets = (
        (
            "Información General",
            {
                "fields": (
                    "name",
                    "ubication",
                )
            },
        ),
        (
            "Código de Integración",
            {
                "fields": ("code",),
                "description": "Ingrese el código HTML o JavaScript que desea integrar en el sitio web.",
            },
        ),
    )

    def code_preview(self, obj):
        """
        Displays a preview of the code in the admin list view.
        """
        if obj.code:
            # Limit the preview to a certain number of characters
            return obj.code
        return "No code"

    code_preview.short_description = "Vista Previa del Código"


admin.site.register(Integration, IntegrationAdmin)
