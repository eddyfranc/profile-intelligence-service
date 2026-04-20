from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer
from .services import process_data


# -------------------------
# POST /api/profiles
# GET  /api/profiles
# -------------------------
@api_view(['POST', 'GET'])
def create_profile(request):

    # =========================
    # POST: Create Profile
    # =========================
    if request.method == 'POST':
        name = request.data.get("name")

        # Missing name
        if name is None:
            return Response(
                {"status": "error", "message": "Missing name"},
                status=400
            )

        # Type validation
        if not isinstance(name, str):
            return Response(
                {"status": "error", "message": "Invalid type"},
                status=422
            )

        name = name.strip().lower()

        if not name:
            return Response(
                {"status": "error", "message": "Missing name"},
                status=400
            )

        # Idempotency check
        existing = Profile.objects.filter(name=name).first()
        if existing:
            return Response({
                "status": "success",
                "message": "Profile already exists",
                "data": ProfileSerializer(existing).data
            }, status=200)

        # External API processing
        try:
            data = process_data(name)
        except Exception as e:
            api_name = str(e)

            if api_name not in ["Genderize", "Agify", "Nationalize"]:
                api_name = "External API"

            return Response({
                "status": "error",
                "message": f"{api_name} returned an invalid response"
            }, status=502)

        # Create profile
        profile = Profile.objects.create(**data)

        return Response({
            "status": "success",
            "data": ProfileSerializer(profile).data
        }, status=201)

    # =========================
    # GET: List Profiles
    # =========================
    queryset = Profile.objects.all()

    gender = request.GET.get("gender")
    country_id = request.GET.get("country_id")
    age_group = request.GET.get("age_group")

    if gender:
        queryset = queryset.filter(gender__iexact=gender)
    if country_id:
        queryset = queryset.filter(country_id__iexact=country_id)
    if age_group:
        queryset = queryset.filter(age_group__iexact=age_group)

    data = ProfileSerializer(queryset, many=True).data

    return Response({
        "status": "success",
        "count": len(data),
        "data": data
    }, status=200)


# -------------------------
# GET /api/profiles/{id}
# -------------------------
@api_view(['GET'])
def get_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response(
            {"status": "error", "message": "Profile not found"},
            status=404
        )

    return Response({
        "status": "success",
        "data": ProfileSerializer(profile).data
    }, status=200)


# -------------------------
# DELETE /api/profiles/{id}
# -------------------------
@api_view(['DELETE'])
def delete_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response(
            {"status": "error", "message": "Profile not found"},
            status=404
        )

    profile.delete()
    return Response(status=204)