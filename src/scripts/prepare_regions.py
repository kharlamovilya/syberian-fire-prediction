import geopandas as gpd
import random
from src.config import SIBERIAN_REGION_NAMES

import sys
print(SIBERIAN_REGION_NAMES)
sys.exit(0)
# Step 1: Load GADM Level 1 — federal subjects
gdf = gpd.read_file("../../data/gadm41_RUS_shp/gadm41_RUS_1.shp")

# Step 2: Filter only Siberian regions
siberia = gdf[gdf['NAME_1'].str.strip().isin(SIBERIAN_REGION_NAMES)].copy()

# Step 3: Add mock weather/environment data
siberia['id'] = siberia.index.astype(str)
siberia['temperature'] = [random.randint(25, 40) for _ in siberia.index]
siberia['humidity'] = [random.randint(10, 60) for _ in siberia.index]
siberia['vegetation_density'] = [round(random.uniform(0.4, 1.0), 2) for _ in siberia.index]

# Step 4: Save result to GeoJSON
output_path = "../../data/siberia_regions.geojson"
siberia.to_file(output_path, driver="GeoJSON")

print(f" Saved enriched Siberia regions to {output_path}")
