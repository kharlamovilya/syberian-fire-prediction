from shapely.geometry import shape

class Region:
    def __init__(self, region_id, geometry, temperature=None, humidity=None, wind_speed=None, wind_direction=None):
        self.region_id = region_id
        self.geometry = shape(geometry)  # Convert GeoJSON to shapely geometry
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

    def contains(self, point):
        return point.within(self.geometry)

    def __repr__(self):
        return f"Region({self.region_id})"
