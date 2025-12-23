import aiohttp
import asyncio
import geopandas as gpd
import pandas as pd
from dotenv import load_dotenv
import os

# File paths
IGNITION_PATH = "../../data/MODIS_C6_1_Russia_Asia_7d.shp"
OUTPUT_PATH = "../../data/ignition_with_weather.geojson"
FALLBACK_CSV = "../outputs/fallback_weather_points.csv"

# API Setup
load_dotenv()
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
API_TEMPLATE = (
    "http://api.weatherapi.com/v1/current.json"
    "?key={key}&q={lat},{lon}&aqi=no"
)

MAX_CONCURRENT = 10
semaphore = asyncio.Semaphore(MAX_CONCURRENT)

success_count = 0
fail_count = 0
fallback_points = []

async def fetch_weather(session, lat, lon, index, total):
    global success_count, fail_count

    async with semaphore:
        url = API_TEMPLATE.format(key=WEATHERAPI_KEY, lat=lat, lon=lon)

        for attempt in range(2):  # try twice
            try:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 502 and attempt == 0:
                        await asyncio.sleep(1)
                        continue  # retry once

                    if resp.status != 200:
                        raise Exception(f"Status {resp.status}")

                    data = await resp.json()
                    current = data.get("current", {})

                    temperature = current.get("temp_c", 20.0)
                    humidity = current.get("humidity", 50.0)
                    wind_speed = round(current.get("wind_kph", 2.0) / 3.6, 2)
                    wind_direction = current.get("wind_degree", 0.0)
                    if index % 250 == 0 or index == total - 1:
                        print(f"🔁 Processed {index + 1}/{total} points...")
                    success_count += 1
                    return {
                        "temperature": temperature,
                        "humidity": humidity,
                        "wind_speed": wind_speed,
                        "wind_direction": wind_direction
                    }

            except Exception as e:
                if attempt == 1:  # only report failure after final try
                    print(f"⚠️ Failed to fetch weather for ({lat:.4f}, {lon:.4f}): {e}")
                    fail_count += 1
                    fallback_points.append((lat, lon))
                    return {
                        "temperature": 20.0,
                        "humidity": 50.0,
                        "wind_speed": 2.0,
                        "wind_direction": 0.0
                    }

async def enrich_points(gdf):
    total = len(gdf)
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_weather(session, row.geometry.y, row.geometry.x, idx, total)
            for idx, row in gdf.iterrows()
        ]
        return await asyncio.gather(*tasks)

# 🔥 Load ignition points
print("🔥 Loading ignition points...")
gdf = gpd.read_file(IGNITION_PATH).to_crs(epsg=4326)
print(f"✅ Loaded {len(gdf)} ignition points")

# 🌦️ Enrich with weather
print("🌦️ Fetching weather for ignition points...")
weather_data = asyncio.run(enrich_points(gdf))

# 🔗 Attach to GeoDataFrame
gdf["temperature"] = [w["temperature"] for w in weather_data]
gdf["humidity"] = [w["humidity"] for w in weather_data]
gdf["wind_speed"] = [w["wind_speed"] for w in weather_data]
gdf["wind_direction"] = [w["wind_direction"] for w in weather_data]
print("🌬️ Wind speeds:")
for w in weather_data:
    print(w["wind_speed"])
# 💾 Save enriched GeoJSON
gdf.to_file(OUTPUT_PATH, driver="GeoJSON")
print(f"✅ Saved enriched ignition points to {OUTPUT_PATH}")

# 💾 Save fallback points
fallback_df = pd.DataFrame(fallback_points, columns=["latitude", "longitude"])
fallback_df.to_csv(FALLBACK_CSV, index=False)
print(f"⚠️ Saved fallback points to {FALLBACK_CSV}")

# 📊 Final Report
print(f"✅ Successes: {success_count}")
print(f"❌ Failures: {fail_count}")
print(f"⚠️ Fallback points: {len(fallback_points)}")
