from django.urls import path

from .views import vocab_list, addvocab, editvocab, review, grade
app_name = 'vocab'

urlpatterns = [
    path('list', vocab_list, name="vocab_list"),
    path('review', review, name="review"),
    path('grade', grade, name="grade"),
    path('add', addvocab, name="addvocab"),
    path('edit/<word>', editvocab, name="editvocab"),
    
]
