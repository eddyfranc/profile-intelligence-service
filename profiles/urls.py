from django.urls import path
from .views import create_profile, list_profiles, get_profile, delete_profile

urlpatterns = [
    # Same endpoint, different methods (IMPORTANT)
    path('profiles', create_profile),   # POST
    path('profiles', list_profiles),    # GET

    # Detail endpoints
    path('profiles/<uuid:id>', get_profile),     # GET by ID
    path('profiles/<uuid:id>', delete_profile),  # DELETE
]