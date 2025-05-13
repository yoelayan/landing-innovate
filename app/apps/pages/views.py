from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages

# Apps
from .models import Brand, Suscriptor, SiteImages, Review, FAQ
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
    return redirect("home")


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

    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Conexiones con externos
        integrations_footer = Integration.objects.filter(ubication="footer")
        integrations_head = Integration.objects.filter(ubication="head")

        brands = Brand.objects.all()
        
        # Format reviews for the template
        reviews_query = Review.objects.all().order_by('-created_at')
        reviews = []
        for review in reviews_query:
            review_data = {
                'name': review.name if review.name else 'Cliente Anónimo',
                'rating': review.rating,
                'comment': review.comment,
                'image': review.image if review.image else None,
            }
            reviews.append(review_data)
            
        # Get and format FAQs for the template
        faqs_query = FAQ.objects.all().order_by('created_at')
        faqs = []
        for i, faq in enumerate(faqs_query):
            faq_data = {
                'id': i + 1,  # For unique IDs in the accordion
                'question': faq.question,
                'answer': faq.answer,
                'is_first': i == 0,  # First FAQ will be expanded
            }
            faqs.append(faq_data)
            
        # If no FAQs exist in the database, provide default ones
        if not faqs:
            faqs = [
                {
                    'id': 1,
                    'question': '¿Qué servicios de marketing digital ofrecen?',
                    'answer': 'Ofrecemos una gama completa de servicios de marketing digital que incluyen gestión de redes sociales, posicionamiento SEO, campañas SEM, email marketing, marketing de contenidos y mucho más. Nuestro enfoque se adapta a las necesidades específicas de tu negocio para maximizar resultados.',
                    'is_first': True,
                },
                {
                    'id': 2,
                    'question': '¿Cuánto tiempo toma desarrollar un sitio web?',
                    'answer': 'El tiempo de desarrollo varía según la complejidad del proyecto. Un sitio web informativo básico puede estar listo en 2-3 semanas, mientras que un e-commerce o un sitio con funcionalidades avanzadas puede tomar entre 1-3 meses. Tras nuestra consulta inicial, te proporcionaremos un cronograma detallado para tu proyecto específico.',
                    'is_first': False,
                },
                {
                    'id': 3,
                    'question': '¿Cómo miden los resultados de sus campañas?',
                    'answer': 'Utilizamos herramientas analíticas avanzadas para medir el rendimiento de todas nuestras campañas. Dependiendo de tus objetivos, podemos monitorear métricas como tráfico web, conversiones, engagement en redes sociales, posicionamiento en buscadores y ROI. Te proporcionamos informes periódicos detallados para que puedas ver cómo nuestras estrategias están impactando positivamente en tu negocio.',
                    'is_first': False,
                },
                {
                    'id': 4,
                    'question': '¿Ofrecen servicios de mantenimiento web?',
                    'answer': 'Sí, ofrecemos planes de mantenimiento web que incluyen actualizaciones de seguridad, copias de seguridad, correcciones de errores, actualizaciones de contenido y soporte técnico. Estos planes son personalizables según las necesidades de tu sitio y garantizan que tu presencia en línea se mantenga actualizada, segura y funcionando de manera óptima.',
                    'is_first': False,
                },
            ]
        
        format_brands = [
            {"src": brand.logo.url, "alt": brand.name} for brand in brands
        ]
        footer_description = "Somos una agencia de marketing digital, desarrollo web y diseño gráfico. <br> ¡Contáctanos y descubre cómo podemos ayudarte a alcanzar tus metas!"
        images = SiteImages.objects.all()
        hero_image = images.filter(code="hero").first().image.url
        graph_image = images.filter(code="graph").first().image.url
        marketing_image = images.filter(code="marketing").first().image.url
        presence_image = images.filter(code="presence").first().image.url
        rentability_image = images.filter(code="rentability").first().image.url
        web_image = images.filter(code="web").first().image.url
        work_group_image = images.filter(code="work_group").first().image.url
        contact_image = images.filter(code="contact").first().image.url

        contact_info = {
            "email": "holainnovate@innova7e.com",
            "phone": "+58 424 144 54 98",
        }
        contact_form = MessagesForm()

        # ? Icons FontAwesome -> https://fontawesome.com/icons
        features = [
            {
                "extra_classes": "text-center shadow",
                "card_icon": "fa-bullseye",
                "card_title": "Análisis y Objetivos",
                "card_text": "Realizamos un diagnóstico integral para definir metas claras, enfocadas en impulsar tu negocio y maximizar resultados.",
            },
            {
                "extra_classes": "text-center shadow",
                "card_icon": "fa-check-circle",
                "card_title": "Estrategia e Implementación",
                "card_text": "Diseñamos un plan de acción personalizado y lo ejecutamos de forma eficiente, priorizando cada tarea según su impacto.",
            },
            {
                "extra_classes": "text-center shadow",
                "card_icon": "fa-chart-line",
                "card_title": "Medición y Optimización",
                "card_text": "Analizamos los resultados para ajustar la estrategia, promoviendo una mejora continua y un mayor retorno de inversión.",
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
                "card_icon": "handshake",
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
                "card_icon": "piggy-bank",
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
                    "card_icon": "fa-brands fa-instagram",
                    "card_title": "Gestión de Marca",
                    "axis": "horizontal",
                    "card_text": "Potencia la reputación de tu negocio aplicando estrategias que refuercen su presencia e impacto en el mercado.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "fas fa-camera",
                    "card_title": "Video Marketing",
                    "axis": "horizontal",
                    "card_text": "Conecta con tu audiencia de forma auténtica a través de contenidos audiovisuales cautivadores que cuentan tu historia.",
                },
                {
                    "icon_classes": "bg-primary",
                    "icon_color": "white",
                    "card_icon": "fas fa-heart",
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
                    "card_icon": "globe",
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
                    "card_icon": "print",
                    "axis": "horizontal",
                    "card_title": "Gigantografía",
                    "axis": "horizontal",
                    "card_text": "Maximiza tu visibilidad con impresiones de gran formato que capten la atención de todos a gran distancia.",
                },
            ],
        }

        # SEO metadata
        page_meta_description = "Potencia tu negocio con Innova7e, expertos en marketing digital, diseño gráfico y desarrollo web en Venezuela. Transformamos tu presencia online para aumentar ventas y visibilidad."
        page_meta_keywords = "marketing digital venezuela, desarrollo web profesional, diseño web responsivo, gestión de redes sociales, seo, sem, posicionamiento web, agencia digital, innova7e"
        
        # Generate structured data for Services (used in Schema.org)
        services_structured_data = []
        for service in [
            {"name": "Marketing Digital", "description": "Marketing Digital profesional para potenciar tu presencia en línea."},
            {"name": "Desarrollo Web", "description": "Soluciones web a medida para tu negocio que convierten visitantes en clientes."},
            {"name": "Diseño Gráfico", "description": "Diseños impactantes que comunican tu identidad de marca y cautivan a tu audiencia."}
        ]:
            services_structured_data.append({
                "@type": "Service",
                "name": service["name"],
                "description": service["description"],
                "provider": {
                    "@type": "Organization",
                    "name": "Innova7e"
                }
            })

        # Update the context
        context.update(
            {
                # SEO metadata
                "page_meta_description": page_meta_description,
                "page_meta_keywords": page_meta_keywords,
                "page_og_image": hero_image,
                "services_structured_data": services_structured_data,
                
                # Existing data
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
                "reviews": reviews,
                "faqs": faqs,
            }
        )

        return context
