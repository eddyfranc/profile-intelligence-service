from django.urls import path
from .views import *

urlpatterns = [
    path('profiles', list_profiles),
    path('profiles/', create_profile),
    path('profiles/<uuid:id>', get_profile),
    path('profiles/<uuid:id>/', delete_profile),
]