from django.urls import path
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

]
