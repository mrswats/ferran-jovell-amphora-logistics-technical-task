import math
from http import HTTPStatus
from typing import Any

import httpx
from django.conf import settings
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response


class AccessPointsSerializer(serializers.Serializer):
    name = serializers.CharField()
    distance = serializers.FloatField()
    euclidean = serializers.FloatField()


class AccessPointsEndpoint(views.APIView):
    def get_top_10_locations(self, latlon: tuple[float, float]) -> list[dict[str, Any]]:
        response = httpx.get(
            "https://places-api.foursquare.com/places/search",
            params={
                "ll": ",".join(map(str, latlon)),
                "sort": "DISTANCE",
            },
            headers={
                "X-Places-Api-Version": "2025-06-17",
                "accept": "application/json",
                "Authorization": f"Bearer {settings.API_KEY}",
            },
        )

        if response.status_code != HTTPStatus.OK:
            raise exceptions.APIException(
                detail="There was an error in the foursquare API",
                code=response.status_code,
            )

        return response.json()["results"]

    def compute_distance(
        self, api_data: list[dict[str, Any]], latlon: tuple[float, float]
    ) -> list[dict[str, Any]]:
        return sorted(
            (
                {
                    "name": place["name"],
                    "distance": place["distance"],
                    "euclidean": math.sqrt(
                        (place["latitude"] - latlon[0]) ** 2
                        + (place["longitude"] - latlon[1]) ** 2
                    ),
                }
                for place in api_data
            ),
            key=lambda o: o["euclidean"],
        )

    def get(self, request: Request, *args, **kwargs) -> Response:
        latlon = (41.39624268234478, 2.150160409597)
        top_10_locations = self.get_top_10_locations(latlon)
        data = self.compute_distance(top_10_locations, latlon)
        serializer = AccessPointsSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
