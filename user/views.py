import random
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *


@api_view(["GET"])
def get_all_users(request):
    try:
        users = User.objects.all()
        users_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined,
                "is_active": user.is_active,
                "full_name": user.first_name,
            }
            for user in users
        ]
        return JsonResponse({"users": users_data}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def get_user_details(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.first_name,
            "mobile": user.profile.mobile,
            "address": user.profile.address,
            "rooms_uploaded": user.profile.rooms_uploaded,
            "date_joined": user.date_joined,
            "is_active": user.is_active,
            "social": [
                {"label": "instagram", "value": "#"},
                {"label": "twitter", "value": "#"},
                {"label": "youtube", "value": "#"},
            ],
            "groups": [group.name for group in user.groups.all()],
        }

        return JsonResponse(user_data, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

@api_view(["GET"])
def get_rooms(request):
    rooms = Room.objects.all()
    room_list = [
        {
            "id": room.pk,
            "title": room.title,
            "type": room.type,
            "price": room.price,
            "thumbnail": room.thumbnail,
            "vendor":room.user.pk,
            "location": {
                "area": "Baner Hills",
                "city": "Pune",
                "distance_to_metro": 2.5,
                "landmark": "Near Prosperity Mall",
            },
            "specifications": {
                "furnishing": "fully_furnished",
                "carpet_area": "950 sqft",
                "preferred_tenants": ["family"],
                "available_from": "next_month",
                "floor": "15th of 20",
            },
            "amenities": [
                "AC",
                "Geyser",
                "TV",
                "Fridge",
                "Washing Machine",
                "Microwave",
                "Gym Access",
                "Swimming Pool",
                "Club House",
            ],
            "ratings": {"overall": 4.8, "total_reviews": 45},
            "tags": ["premium", "family_friendly", "fully_furnished"],
        }
        for room in rooms
    ]
    response = {"status": "success", "count": len(room_list), "rooms": room_list}
    return Response(response)
