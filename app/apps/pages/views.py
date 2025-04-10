from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages

# Apps
from .models import Brand, Suscriptor, SiteImages
from apps.external_integrations.models import Integration
from .forms import MessagesForm

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""





def suscriptor_process_form(request):
    if request.method == "POST":

        email = request.POST.get("email")
        if email:
            try:
                Suscriptor.objects.create(email=email)
            except Exception:
                messages.error(request, "Ya te has suscrito antes")
            else:
                messages.success(request, "Te has suscrito a nuestras noticias")
    return redirect("landing-page")


class HomePageView(TemplateView):
    template_name = "pages_home.html"

    def post(self, request, *args, **kwargs):
        form = MessagesForm(request.POST)
        if form.is_valid():
            messages.success(request, "Mensaje enviado correctamente")

            form.save()
        else:

            context = self.get_context_data(**kwargs)
            context.update(
                {
                    "contact_form": form,
                }
            )
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = super().get_context_data(**kwargs)
        integrations_footer = Integration.objects.filter(ubication="footer")
        integrations_head = Integration.objects.filter(ubication="head")

        brands = Brand.objects.all()
        format_brands = [{"src": brand.logo.url, "alt": brand.name} for brand in brands]
        footer_description = "Somos una agencia de marketing digital, desarrollo web y diseño gráfico. <br> ¡Contáctanos y descubre cómo podemos ayudarte a alcanzar tus metas!"
        images = SiteImages.objects.all()
        hero_image = images.filter(code="hero").first()
        graph_image = images.filter(code="graph").first()
        marketing_image = images.filter(code="marketing").first()
        presence_image = images.filter(code="presence").first()
        rentability_image = images.filter(code="rentability").first()
        web_image = images.filter(code="web").first()
        work_group_image = images.filter(code="work_group").first()
        contact_image = images.filter(code="contact").first()

        contact_info = {
            "email": "holainnovate@innova7e.com",
            "phone": "+58 424 144 54 98",
        }
        contact_form = MessagesForm()

        # ? Icons Tabler -> https://tabler.io/icons
        features = [
            {
                "extra_classes": "text-center shadow",
                "card_icon": "target-arrow",
                "card_title": "Análisis y Objetivos",
                "card_text": "Realizamos un diagnóstico integral para definir metas claras, enfocadas en impulsar tu negocio y maximizar resultados.",
            },
            {
                "extra_classes": "text-center shadow",
                "card_icon": "checklist",
                "card_title": "Estrategia e Implementación",
                "card_text": "Diseñamos un plan de acción personalizado y lo ejecutamos de forma eficiente, priorizando cada tarea según su impacto.",
            },
            {
                "extra_classes": "text-center shadow",
                "card_icon": "chart-bar",
                "card_title": "Medición y Optimización",
                "card_text": "Analizamos los resultados para ajustar la estrategia, promoviendo una mejora continua y un mayor retorno de inversión.",
            },
        ]
        features_2 = [
            {
                "extra_classes": "card-topper text-center",
                "card_image": rentability_image,
                "card_title": "Genera más rentabilidad",
                "card_text": "Creamos estrategias orientadas a optimizar tus recursos y aumentar tus ingresos de manera sostenible.",
            },
            {
                "extra_classes": "card-topper text-center",
                "card_image": presence_image,
                "card_title": "Aumenta tu presencia",
                "card_text": "Fortalecemos tu imagen de marca y alcance digital, logrando que tu negocio destaque ante la competencia.",
            },
            {
                "extra_classes": "card-topper text-center",
                "card_image": work_group_image,
                "card_title": "Trabajamos codo a codo contigo",
                "card_text": "Brindándote atención personalizada y soluciones diseñadas a tu medida.",
            },
        ]
        features_3 = [
            {
                "extra_classes": "text-center",
                "card_icon": "clock",
                "card_title": "Acceso a soporte personalizado",
                "card_text": "Atendemos tus consultas y necesidades en cualquier momento, asegurando una respuesta rápida y efectiva.",
            },
            {
                "extra_classes": "text-center",
                "card_icon": "heart-handshake",
                "card_title": "Consultoría Especializada",
                "card_text": "Analizamos tu modelo de negocio en detalle y diseñamos soluciones a la medida para cada desafío que enfrentes.",
            },
            {
                "extra_classes": "text-center",
                "card_icon": "bolt",
                "card_title": "Procesos Eficientes",
                "card_text": "Aprovechamos tecnología y metodologías efectivas, evitando costos innecesarios.",
            },
            {
                "extra_classes": "text-center",
                "card_icon": "pig-money",
                "card_title": "Recursos Óptimos",
                "card_text": "Optimizamos tus recursos para maximizar el retorno de tu inversión.",
            },
        ]

        # ? Services
        # ? title, subtitle, services: 3 mini section

        services_1 = {
            "title": "Marketing Digital",
            "subtitle": "Prospecta tu imagen y comercializa tus productos.",
            "cards": [
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "brand-instagram",
                    "card_title": "Gestión de Marca",
                    "axis": "horizontal",
                    "card_text": "Potencia la reputación de tu negocio aplicando estrategias que refuercen su presencia e impacto en el mercado.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "camera",
                    "card_title": "Video Marketing",
                    "axis": "horizontal",
                    "card_text": "Conecta con tu audiencia de forma auténtica a través de contenidos audiovisuales cautivadores que cuentan tu historia.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "heart",
                    "card_title": "Branding",
                    "axis": "horizontal",
                    "card_text": "Diseña la esencia de tu negocio al crear valores, identidad visual y voz propia, logrando una conexión emocional con tu público.",
                },
            ],
        }
        services_2 = {
            "title": "Desarrollo web",
            "subtitle": "Crea la presencia digital que tu negocio necesita.",
            "cards": [
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "world-www",
                    "axis": "horizontal",
                    "is_reverse": True,
                    "card_title": "Páginas Web",
                    "card_text": "Brinda a tu negocio un escaparate digital atractivo y funcional para captar clientes las 24 horas del día.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "server",
                    "axis": "horizontal",
                    "is_reverse": True,
                    "card_title": "Hosting y Dominio",
                    "card_text": "Asegura tu espacio en línea con un nombre memorable y un servicio confiable que mantenga tu sitio siempre activo.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "tools",
                    "axis": "horizontal",
                    "is_reverse": True,
                    "card_title": "Diseño UI - UX",
                    "card_text": "Crea interfaces fáciles de usar y agradables a la vista, para una experiencia de navegación que tus visitantes recordarán.",
                },
            ],
        }
        services_3 = {
            "title": "Diseño Gráfico",
            "subtitle": "Crea diseños que comuniquen y cautiven.",
            "cards": [
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "flag",
                    "axis": "horizontal",
                    "card_title": "Desarrollo de Identidad",
                    "card_text": "Plasma la personalidad de tu negocio en logotipos y elementos visuales que destaquen y conecten con tu audiencia.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "clipboard",
                    "axis": "horizontal",
                    "card_title": "Papelería Corporativa",
                    "card_text": "Da coherencia a tu marca con tarjetas de presentación, sobres y otros elementos que transmitan profesionalismo.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "printer",
                    "axis": "horizontal",
                    "card_title": "Gigantografía",
                    "card_text": "Maximiza tu visibilidad con impresiones de gran formato que capten la atención de todos a gran distancia.",
                },
            ],
        }

        # Update the context
        context.update(
            {
                
                "navbar_full": True,
                "active_url": self.request.path,
                "page_title": "POTENCIA TU NEGOCIO Y DESTACA EN EL MUNDO DIGITAL",
                "page_subtitle": "¡Da el siguiente paso hacia el éxito! Ponte en contacto y descubre cómo nuestros servicios pueden impulsar tu negocio a lo más alto.",
                "brands": format_brands,
                "features": features,
                "features_2": features_2,
                "features_3": features_3,
                "features__title": "Protege tus inversiones con precisión absoluta.",
                "features__subtitle": "Nuestro equipo experto te ofrece asesoría personalizada, ayudándote a impulsar tu negocio con confianza.",
                "features_2__title": "Ahorra Tiempo y Dinero con Nosotros.",
                "features_2__subtitle": "Empieza a fortalecer tu presencia en el mercado y cuenta con el respaldo de nuestro equipo especializado.",
                "services_1": services_1,
                "services_2": services_2,
                "services_3": services_3,
                "footer_description": footer_description,
                "hero_image": hero_image,
                "graph_image": graph_image,
                "marketing_image": marketing_image,
                "presence_image": presence_image,
                "rentability_image": rentability_image,
                "web_image": web_image,
                "work_group_image": work_group_image,
                "contact_image": contact_image,
                "contact_info": contact_info,
                "contact_form": contact_form,
                "integrations_footer": integrations_footer,
                "integrations_head": integrations_head,
            }
        )

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
