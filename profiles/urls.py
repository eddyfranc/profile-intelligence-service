from django.urls import path
from .views import create_profile, get_profile, delete_profile

urlpatterns = [
    # POST /api/profiles
    # GET  /api/profiles (handled inside same view)
    path('profiles', create_profile),

    # GET /api/profiles/{id}
    path('profiles/<uuid:id>', get_profile),

    # DELETE /api/profiles/{id}
    path('profiles/<uuid:id>', delete_profile),
]