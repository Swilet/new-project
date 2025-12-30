from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Travel

class TravelListView(ListView):
    model = Travel
    template_name = 'travel/travel_list.html'
    context_object_name = 'travels'
    ordering = ['-created_at']

travel_list = TravelListView.as_view()

class TravelDetailView(DetailView):
    model = Travel
    template_name = 'travel/travel_detail.html'

travel_detail = TravelDetailView.as_view()