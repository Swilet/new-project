from django.urls import path
from .views import NoteListView

app_name = 'notes'

urlpatterns = [
    path('', NoteListView.as_view(), name='note_list'),
]
