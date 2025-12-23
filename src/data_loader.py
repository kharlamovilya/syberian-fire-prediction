import geopandas as gpd
from region import Region

def load_regions(file_path):
    gdf = gpd.read_file(file_path)

    regions = []
    for _, row in gdf.iterrows():
        region = Region(
            region_id=row["NAME_1"],
            geometry=row["geometry"],
            temperature=row["temperature"],
            humidity=row["humidity"],
            wind_speed=row.get("wind_speed", 0.0),
            wind_direction=row.get("wind_direction", "N")
        )
        regions.append(region)

    return regions
