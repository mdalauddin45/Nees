from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'
    