from django.urls import path
from . import views
urlpatterns =[
    path('', views.home, name='home'),
    path('add_form_parent', views.add_form_parent, name='add_form_parent'),
    path('add_form_fields/<int:pk>', views.add_form_fields, name='add_form_fields'),
    path('delete_form_field/<int:pk>', views.delete_form_field, name='delete_form_field'),
    path('form_view/<str:unique_id>', views.form_view, name='form_view'),
    path('form_submit/<str:unique_id>', views.form_submit, name='form_submit'),
    path('responses/<int:pk>', views.responses, name='responses'),
    path('accept_responses_toggle/<int:pk>', views.accept_responses_toggle, name='accept_responses_toggle'),
    path('forms', views.forms, name='forms'),
    path('delete_form/<int:pk>', views.delete_form, name='delete_form')
]