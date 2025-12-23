import geopandas as gpd
import config
from data_loader import load_regions
from ignition_point import IgnitionPoint
from simulator import FireSimulator
from map_renderer import render_fire_map_html
from spread_loader import load_spread_points_from_json

# Step 1: Load enriched regions
regions = load_regions(config.ENRICHED_REGIONS_PATH)
print("Loaded region IDs:")
for r in regions:
    print(f" - {r.region_id}")

# Step 2: Load enriched ignition points
print("Loading ignition points with weather...")
gdf = gpd.read_file(config.ENRICHED_IGNITIONS_PATH).to_crs(epsg=4326)

ignition_points = []
for _, row in gdf.iterrows():
    pt = IgnitionPoint(
        x=row.geometry.x,
        y=row.geometry.y,
        temperature=row.get("temperature", 20.0),
        humidity=row.get("humidity", 50.0),
        wind_speed=row.get("wind_speed", 2.0),
        wind_direction=row.get("wind_direction", 0.0)
    )
    ignition_points.append(pt)

print(f"✓ {len(ignition_points)} ignition points loaded")

# Step 3: Filter points within selected regions
region_polygons = [r.geometry for r in regions]
filtered_points = [pt for pt in ignition_points if any(pt.to_point().within(poly) for poly in region_polygons)]
print(f"✓ {len(filtered_points)} fire points inside selected regions")

# Step 4: Prepare NDVI loader
from ndvi_loader import NDVILoader
ndvi_loader = NDVILoader(config.NDVI_PATH)

# Step 5: Run fire simulation
sim = FireSimulator(regions, config.FIRE_SPREAD_PATH)
sim.simulate_fire(
    ignition_points=filtered_points,
    ndvi_loader=ndvi_loader,
    steps=1,
    risk_threshold=0.3,
    max_distance=0.2
)
ndvi_loader.close()


# Step 6: Render fire map
print("Rendering Map")
spread_gdf = load_spread_points_from_json(config.FIRE_SPREAD_PATH)
render_fire_map_html(
    regions=regions,
    ignition_points=filtered_points,
    spread_points=list(spread_gdf.itertuples()),
    output_path=config.MAP_OUTPUT_PATH
)
