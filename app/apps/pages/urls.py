from django.urls import path
from django.views.generic.base import TemplateView
from .views import HomePageView, suscriptor_process_form


urlpatterns = [
    
    path(
        "",
        HomePageView.as_view(),
        name="home",
    ),
    path(
        "suscriptor/",
        suscriptor_process_form,
        name="suscriptor",
    ),
    # SEO routes
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_txt",
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml"),
        name="sitemap_xml",
    ),
]
