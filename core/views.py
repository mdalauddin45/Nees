from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from room.models import Room
# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.all()
        context['rooms'] = rooms
        return context
class AboutView(TemplateView):
    template_name = 'about.html'
class RoomView(TemplateView):
    template_name = 'rooms.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rooms = Room.objects.all()
        context['rooms'] = rooms
        return context
    
