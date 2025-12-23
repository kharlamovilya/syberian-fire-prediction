# config.py

SIBERIAN_REGION_NAMES = [
    "Khanty", "Tomsk", "Novosibirsk",
    "Kemerovo", "Krasnoyarsk", "Irkutsk", "Khakass",
    "Sakha", "Amur", "Tuva", "Buryat", "Zabaykal'ye", "Altay"
]

ENRICHED_REGIONS_PATH = "../data/siberia_regions_with_weather.geojson"
ENRICHED_IGNITIONS_PATH = "../data/ignition_with_weather.geojson"
NDVI_PATH = "../data/modis_ndvi_siberia_2025-06.tif"

FIRE_SPREAD_PATH = "../outputs/spread_points.json"
MAP_OUTPUT_PATH = "../outputs/fire_map.html"

WIND_RANDOM_SPREAD = 16

MAP_CLUSTERING = 8
