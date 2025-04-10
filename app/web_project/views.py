from django.views.generic import TemplateView

class MiscPagesView(TemplateView):
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        return context