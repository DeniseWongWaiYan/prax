from django.urls import path

from .views import vocab_list, addvocab
app_name = 'vocab'

urlpatterns = [
    path('list', vocab_list, name="vocab_list"),
    path('add', addvocab, name="addvocab"),
 
]
