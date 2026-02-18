#! /usr/bin/env python
from __future__ import annotations

import os
import pprint

import httpx

API_KEY = os.getenv("API_KEY")


def get_top_10_locations() -> list[str]:
    response = httpx.get(
        (
            "https://places-api.foursquare.com/places/search"
            "?ll=41.39624268234478,2.150160409597&sort=DISTANCE"
        ),
        headers={
            "X-Places-Api-Version": "2025-06-17",
            "accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    return [place["name"] for place in response.json()["results"]]


def main() -> int:
    pprint.pprint(get_top_10_locations())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
