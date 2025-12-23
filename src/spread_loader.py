import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import json

def load_spread_points_from_json(json_path):
    """
    Load fire spread points from a saved JSON file into a GeoDataFrame.

    Parameters:
    - json_path (str): Path to the JSON file containing spread points.

    Returns:
    - GeoDataFrame: containing columns ['temperature', 'humidity', 'wind_speed', 'wind_direction', 'ndvi', 'step', 'geometry']
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df["geometry"] = df.apply(lambda row: Point(row["x"], row["y"]), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
    return gdf
