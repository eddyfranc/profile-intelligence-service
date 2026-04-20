# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from .serializers import ProfileSerializer
from .services import process_data

@api_view(['POST'])
def create_profile(request):
    name = request.data.get("name")

    if not name:
        return Response({"status": "error", "message": "Missing name"}, status=400)

    if not isinstance(name, str):
        return Response({"status": "error", "message": "Invalid type"}, status=422)

    name = name.lower()

    # Idempotency check
    existing = Profile.objects.filter(name=name).first()
    if existing:
        return Response({
            "status": "success",
            "message": "Profile already exists",
            "data": ProfileSerializer(existing).data
        }, status=200)

    try:
        data = process_data(name)
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"{str(e)} returned an invalid response"
        }, status=502)

    profile = Profile.objects.create(**data)

    return Response({
        "status": "success",
        "data": ProfileSerializer(profile).data
    }, status=201)

@api_view(['GET'])
def get_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response({"status": "error", "message": "Profile not found"}, status=404)

    return Response({"status": "success", "data": ProfileSerializer(profile).data})



@api_view(['GET'])
def list_profiles(request):
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

    data = [{
        "id": p.id,
        "name": p.name,
        "gender": p.gender,
        "age": p.age,
        "age_group": p.age_group,
        "country_id": p.country_id
    } for p in queryset]

    return Response({
        "status": "success",
        "count": len(data),
        "data": data
    })



@api_view(['DELETE'])
def delete_profile(request, id):
    try:
        profile = Profile.objects.get(id=id)
        profile.delete()
        return Response(status=204)
    except Profile.DoesNotExist:
        return Response({"status": "error", "message": "Profile not found"}, status=404)
    



    