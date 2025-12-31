from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Travel

class TravelListView(ListView):
    model = Travel
    template_name = 'travel/travel_list.html'
    context_object_name = 'travels'
    ordering = ['-created_at']

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags')

travel_list = TravelListView.as_view()

class TravelDetailView(DetailView):
    model = Travel
    template_name = 'travel/travel_detail.html'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('tags')

travel_detail = TravelDetailView.as_view()